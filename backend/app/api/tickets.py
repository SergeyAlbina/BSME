from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from sqlalchemy.orm import selectinload
from typing import List, Optional
from datetime import datetime
import aiofiles
import os
from uuid import uuid4

from ..core.database import get_db
from ..core.config import settings
from ..models.ticket import Ticket, Comment, TicketHistory, Attachment
from ..models.user import User
from ..schemas.ticket import (
    TicketCreate,
    TicketUpdate,
    TicketResponse,
    TicketDetailResponse,
    CommentCreate,
    CommentResponse,
)
from .users import get_current_user

router = APIRouter()


def generate_ticket_number(year: int, count: int) -> str:
    """Генерация номера заявки"""
    return f"IT-{year}-{count:04d}"


async def create_history_entry(
    db: AsyncSession,
    ticket_id: int,
    user_id: int,
    action: str,
    old_value: Optional[str] = None,
    new_value: Optional[str] = None,
):
    """Создание записи в истории"""
    history = TicketHistory(
        ticket_id=ticket_id,
        user_id=user_id,
        action=action,
        old_value=old_value,
        new_value=new_value,
    )
    db.add(history)


@router.post("/", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
async def create_ticket(
    ticket_data: TicketCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Создание новой заявки"""
    # Генерация номера заявки
    current_year = datetime.now().year
    result = await db.execute(
        select(Ticket).where(Ticket.ticket_number.like(f"IT-{current_year}-%"))
    )
    existing_tickets = result.scalars().all()
    ticket_number = generate_ticket_number(current_year, len(existing_tickets) + 1)

    # Создание заявки
    new_ticket = Ticket(
        ticket_number=ticket_number,
        title=ticket_data.title,
        description=ticket_data.description,
        category=ticket_data.category,
        priority=ticket_data.priority,
        location=ticket_data.location,
        equipment_type=ticket_data.equipment_type,
        creator_id=current_user.id,
        status="new",
    )

    db.add(new_ticket)
    await db.flush()

    # Создание записи в истории
    await create_history_entry(
        db, new_ticket.id, current_user.id, "created", None, f"Заявка создана: {ticket_data.title}"
    )

    await db.commit()
    await db.refresh(new_ticket)

    return new_ticket


@router.get("/", response_model=List[TicketResponse])
async def get_tickets(
    skip: int = 0,
    limit: int = 50,
    status: Optional[str] = None,
    category: Optional[str] = None,
    priority: Optional[str] = None,
    assigned_to_me: bool = False,
    created_by_me: bool = False,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Получение списка заявок с фильтрацией"""
    query = select(Ticket)

    # Фильтры
    if status:
        query = query.where(Ticket.status == status)
    if category:
        query = query.where(Ticket.category == category)
    if priority:
        query = query.where(Ticket.priority == priority)
    if assigned_to_me:
        query = query.where(Ticket.assigned_to == current_user.id)
    if created_by_me:
        query = query.where(Ticket.creator_id == current_user.id)

    # Для обычных пользователей показываем только их заявки
    if current_user.role == "user":
        query = query.where(Ticket.creator_id == current_user.id)

    query = query.offset(skip).limit(limit).order_by(Ticket.created_at.desc())

    result = await db.execute(query)
    tickets = result.scalars().all()

    return tickets


@router.get("/{ticket_id}", response_model=TicketDetailResponse)
async def get_ticket(
    ticket_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Получение детальной информации о заявке"""
    result = await db.execute(
        select(Ticket)
        .where(Ticket.id == ticket_id)
        .options(
            selectinload(Ticket.comments),
            selectinload(Ticket.history),
            selectinload(Ticket.attachments),
        )
    )
    ticket = result.scalar_one_or_none()

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заявка не найдена",
        )

    # Проверка прав доступа
    if current_user.role == "user" and ticket.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для просмотра этой заявки",
        )

    return ticket


@router.patch("/{ticket_id}", response_model=TicketResponse)
async def update_ticket(
    ticket_id: int,
    ticket_data: TicketUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Обновление заявки"""
    result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    ticket = result.scalar_one_or_none()

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заявка не найдена",
        )

    # Проверка прав
    if current_user.role == "user" and ticket.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав",
        )

    # Обновление полей и создание истории
    for field, value in ticket_data.model_dump(exclude_unset=True).items():
        if value is not None:
            old_value = getattr(ticket, field)
            if old_value != value:
                setattr(ticket, field, value)
                await create_history_entry(
                    db, ticket.id, current_user.id, f"{field}_changed", str(old_value), str(value)
                )

    # Если статус изменен на closed, установить дату закрытия
    if ticket_data.status == "closed" and not ticket.closed_at:
        ticket.closed_at = datetime.now()

    await db.commit()
    await db.refresh(ticket)

    return ticket


@router.post("/{ticket_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def add_comment(
    ticket_id: int,
    comment_text: str,
    is_internal: bool = False,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Добавление комментария к заявке"""
    result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    ticket = result.scalar_one_or_none()

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заявка не найдена",
        )

    # Только инженеры и админы могут оставлять внутренние комментарии
    if is_internal and current_user.role not in ["engineer", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для создания внутренних комментариев",
        )

    new_comment = Comment(
        ticket_id=ticket_id,
        user_id=current_user.id,
        comment_text=comment_text,
        is_internal="true" if is_internal else "false",
    )

    db.add(new_comment)
    await db.flush()

    # Создание записи в истории
    await create_history_entry(
        db, ticket_id, current_user.id, "commented", None, comment_text[:100]
    )

    await db.commit()
    await db.refresh(new_comment)

    return new_comment


@router.post("/{ticket_id}/assign", response_model=TicketResponse)
async def assign_ticket(
    ticket_id: int,
    engineer_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Назначение заявки на инженера"""
    if current_user.role not in ["engineer", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав",
        )

    result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    ticket = result.scalar_one_or_none()

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заявка не найдена",
        )

    # Если engineer_id не указан, назначаем на себя
    if engineer_id is None:
        engineer_id = current_user.id

    old_assigned = ticket.assigned_to
    ticket.assigned_to = engineer_id

    # Обновляем статус, если заявка была новой
    if ticket.status == "new":
        ticket.status = "in_progress"

    await create_history_entry(
        db, ticket_id, current_user.id, "assigned", str(old_assigned), str(engineer_id)
    )

    await db.commit()
    await db.refresh(ticket)

    return ticket
