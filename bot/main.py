import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery

from config import settings
from keyboards import (
    main_menu_keyboard,
    category_keyboard,
    priority_keyboard,
    ticket_action_keyboard,
    cancel_keyboard,
)
from database import async_session_maker
from sqlalchemy import select
import sys
import os

# Добавляем путь к backend для импорта моделей
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))
from app.models.user import User
from app.models.ticket import Ticket, Comment

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


# Состояния для создания заявки
class TicketForm(StatesGroup):
    waiting_for_title = State()
    waiting_for_description = State()
    waiting_for_category = State()
    waiting_for_priority = State()
    waiting_for_location = State()
    waiting_for_equipment = State()


# Состояние для добавления комментария
class CommentForm(StatesGroup):
    waiting_for_comment = State()
    ticket_id = None


async def get_or_create_user(telegram_id: int, username: str, full_name: str):
    """Получить или создать пользователя"""
    async with async_session_maker() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()

        if not user:
            user = User(
                telegram_id=telegram_id,
                username=username,
                full_name=full_name,
                role="user",
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)

        return user


@dp.message(Command("start"))
async def cmd_start(message: Message):
    """Обработка команды /start"""
    user = await get_or_create_user(
        message.from_user.id,
        message.from_user.username,
        message.from_user.full_name,
    )

    await message.answer(
        f"👋 Привет, {user.full_name}!\n\n"
        "Я бот для управления заявками на IT поддержку.\n\n"
        "Используйте меню ниже для работы с заявками.",
        reply_markup=main_menu_keyboard(),
    )


@dp.message(Command("help"))
@dp.message(F.text == "ℹ️ Помощь")
async def cmd_help(message: Message):
    """Помощь"""
    help_text = """
📖 <b>Доступные команды:</b>

/start - Начать работу
/help - Показать эту справку
/mytickets - Мои заявки

<b>Кнопки меню:</b>
📝 Создать заявку - создание новой заявки
📋 Мои заявки - просмотр ваших заявок

<b>Категории заявок:</b>
🖥 Оборудование - ремонт и обслуживание техники
💾 ПО - помощь с программами

<b>Приоритеты:</b>
🔴 Критический - срочно
🟠 Высокий - важно
🟡 Средний - обычная заявка
🟢 Низкий - не срочно
    """
    await message.answer(help_text, parse_mode="HTML")


@dp.message(F.text == "📝 Создать заявку")
async def start_create_ticket(message: Message, state: FSMContext):
    """Начало создания заявки"""
    await message.answer(
        "📝 <b>Создание новой заявки</b>\n\n"
        "Введите краткое описание проблемы (заголовок заявки):",
        reply_markup=cancel_keyboard(),
        parse_mode="HTML",
    )
    await state.set_state(TicketForm.waiting_for_title)


@dp.message(TicketForm.waiting_for_title)
async def process_title(message: Message, state: FSMContext):
    """Обработка заголовка заявки"""
    await state.update_data(title=message.text)
    await message.answer(
        "📄 Теперь опишите проблему подробнее:",
        reply_markup=cancel_keyboard(),
    )
    await state.set_state(TicketForm.waiting_for_description)


@dp.message(TicketForm.waiting_for_description)
async def process_description(message: Message, state: FSMContext):
    """Обработка описания заявки"""
    await state.update_data(description=message.text)
    await message.answer(
        "📂 Выберите категорию заявки:",
        reply_markup=category_keyboard(),
    )
    await state.set_state(TicketForm.waiting_for_category)


@dp.callback_query(F.data.startswith("category:"))
async def process_category(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора категории"""
    category = callback.data.split(":")[1]
    await state.update_data(category=category)

    category_text = "🖥 Оборудование" if category == "hardware" else "💾 Программное обеспечение"
    await callback.message.edit_text(f"✅ Выбрана категория: {category_text}")

    await callback.message.answer(
        "⚡ Выберите приоритет заявки:",
        reply_markup=priority_keyboard(),
    )
    await state.set_state(TicketForm.waiting_for_priority)
    await callback.answer()


@dp.callback_query(F.data.startswith("priority:"))
async def process_priority(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора приоритета"""
    priority = callback.data.split(":")[1]
    await state.update_data(priority=priority)

    priority_text = {
        "critical": "🔴 Критический",
        "high": "🟠 Высокий",
        "medium": "🟡 Средний",
        "low": "🟢 Низкий",
    }[priority]

    await callback.message.edit_text(f"✅ Выбран приоритет: {priority_text}")

    await callback.message.answer(
        "📍 Укажите местоположение оборудования (или напишите 'нет', если не применимо):",
    )
    await state.set_state(TicketForm.waiting_for_location)
    await callback.answer()


@dp.message(TicketForm.waiting_for_location)
async def process_location(message: Message, state: FSMContext):
    """Обработка местоположения"""
    location = None if message.text.lower() in ['нет', 'no', '-'] else message.text
    await state.update_data(location=location)

    data = await state.get_data()
    if data.get('category') == 'hardware':
        await message.answer(
            "🖥 Укажите тип оборудования (принтер, компьютер, монитор и т.д.):",
        )
        await state.set_state(TicketForm.waiting_for_equipment)
    else:
        await create_ticket_in_db(message, state)


@dp.message(TicketForm.waiting_for_equipment)
async def process_equipment(message: Message, state: FSMContext):
    """Обработка типа оборудования"""
    equipment_type = message.text
    await state.update_data(equipment_type=equipment_type)
    await create_ticket_in_db(message, state)


async def create_ticket_in_db(message: Message, state: FSMContext):
    """Создание заявки в БД"""
    data = await state.get_data()

    async with async_session_maker() as session:
        # Получаем пользователя
        result = await session.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )
        user = result.scalar_one()

        # Генерируем номер заявки
        from datetime import datetime
        current_year = datetime.now().year
        result = await session.execute(
            select(Ticket).where(Ticket.ticket_number.like(f"IT-{current_year}-%"))
        )
        existing_tickets = result.scalars().all()
        ticket_number = f"IT-{current_year}-{len(existing_tickets) + 1:04d}"

        # Создаем заявку
        new_ticket = Ticket(
            ticket_number=ticket_number,
            title=data['title'],
            description=data.get('description'),
            category=data['category'],
            priority=data['priority'],
            location=data.get('location'),
            equipment_type=data.get('equipment_type'),
            creator_id=user.id,
            status='new',
        )

        session.add(new_ticket)
        await session.commit()
        await session.refresh(new_ticket)

        # Формируем сообщение
        category_emoji = "🖥" if new_ticket.category == "hardware" else "💾"
        priority_emoji = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}[new_ticket.priority]

        message_text = f"""
✅ <b>Заявка создана!</b>

📋 Номер: <code>{new_ticket.ticket_number}</code>
{category_emoji} Категория: {new_ticket.category}
{priority_emoji} Приоритет: {new_ticket.priority}
📝 Заголовок: {new_ticket.title}
        """

        await message.answer(
            message_text,
            parse_mode="HTML",
            reply_markup=main_menu_keyboard(),
        )

    await state.clear()


@dp.message(F.text == "📋 Мои заявки")
@dp.message(Command("mytickets"))
async def show_my_tickets(message: Message):
    """Показать мои заявки"""
    async with async_session_maker() as session:
        # Получаем пользователя
        result = await session.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )
        user = result.scalar_one_or_none()

        if not user:
            await message.answer("❌ Пользователь не найден. Используйте /start")
            return

        # Получаем заявки пользователя
        result = await session.execute(
            select(Ticket)
            .where(Ticket.creator_id == user.id)
            .order_by(Ticket.created_at.desc())
            .limit(10)
        )
        tickets = result.scalars().all()

        if not tickets:
            await message.answer(
                "📋 У вас пока нет заявок.\n\n"
                "Нажмите '📝 Создать заявку' для создания новой.",
                reply_markup=main_menu_keyboard(),
            )
            return

        # Формируем список заявок
        tickets_text = "📋 <b>Ваши заявки:</b>\n\n"

        status_emoji = {
            "new": "🆕",
            "in_progress": "⏳",
            "resolved": "✅",
            "closed": "🔒",
        }

        for ticket in tickets:
            status = status_emoji.get(ticket.status, "❓")
            tickets_text += f"{status} <code>{ticket.ticket_number}</code> - {ticket.title}\n"
            tickets_text += f"   Статус: {ticket.status}\n\n"

        await message.answer(tickets_text, parse_mode="HTML")


@dp.callback_query(F.data == "cancel")
async def cancel_action(callback: CallbackQuery, state: FSMContext):
    """Отмена действия"""
    await state.clear()
    await callback.message.answer(
        "❌ Действие отменено.",
        reply_markup=main_menu_keyboard(),
    )
    await callback.answer()


async def main():
    """Запуск бота"""
    logger.info("🤖 Запуск бота...")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
