from datetime import datetime
import uuid
from sqlalchemy import String, DateTime, UUID, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column
from ..database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    phone: Mapped[str] = mapped_column(String, unique=True, index=True)
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    preferences: Mapped[dict] = mapped_column(JSON, default=lambda: {"notifications": {"email": True, "sms": True, "push": True}})
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<User(name={self.name}, email={self.email})>"
