from sqlalchemy import Column, Integer, String, BigInteger, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, nullable=True, index=True)
    username = Column(String(100), unique=True, nullable=True, index=True)
    full_name = Column(String(200))
    email = Column(String(100), unique=True, nullable=True, index=True)
    hashed_password = Column(String(255), nullable=True)
    role = Column(String(20), default="user")  # user, engineer, admin
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    created_tickets = relationship("Ticket", back_populates="creator", foreign_keys="Ticket.creator_id")
    assigned_tickets = relationship("Ticket", back_populates="assigned_engineer", foreign_keys="Ticket.assigned_to")
    comments = relationship("Comment", back_populates="user")
    history_entries = relationship("TicketHistory", back_populates="user")
    attachments = relationship("Attachment", back_populates="uploaded_by_user")

    def __repr__(self):
        return f"<User {self.username or self.full_name}>"
