from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class TicketBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    description: Optional[str] = None
    category: str = Field(..., pattern="^(hardware|software)$")
    priority: str = Field(default="medium", pattern="^(low|medium|high|critical)$")
    location: Optional[str] = None
    equipment_type: Optional[str] = None


class TicketCreate(TicketBase):
    pass


class TicketUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = None
    category: Optional[str] = Field(None, pattern="^(hardware|software)$")
    priority: Optional[str] = Field(None, pattern="^(low|medium|high|critical)$")
    status: Optional[str] = Field(None, pattern="^(new|in_progress|resolved|closed)$")
    assigned_to: Optional[int] = None
    location: Optional[str] = None
    equipment_type: Optional[str] = None


class TicketResponse(TicketBase):
    id: int
    ticket_number: str
    status: str
    creator_id: int
    assigned_to: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CommentBase(BaseModel):
    comment_text: str = Field(..., min_length=1)
    is_internal: bool = False


class CommentCreate(CommentBase):
    ticket_id: int


class CommentResponse(CommentBase):
    id: int
    ticket_id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class TicketHistoryResponse(BaseModel):
    id: int
    ticket_id: int
    user_id: int
    action: str
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class AttachmentResponse(BaseModel):
    id: int
    ticket_id: int
    file_name: str
    file_type: Optional[str] = None
    uploaded_by: int
    created_at: datetime

    class Config:
        from_attributes = True


class TicketDetailResponse(TicketResponse):
    comments: List[CommentResponse] = []
    history: List[TicketHistoryResponse] = []
    attachments: List[AttachmentResponse] = []
