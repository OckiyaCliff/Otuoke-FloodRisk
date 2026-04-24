from datetime import datetime
import uuid
from sqlalchemy import String, DateTime, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from ..database import Base


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    prediction_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("predictions.id"))
    
    severity: Mapped[str] = mapped_column(String)  # Low, Medium, High, Critical
    channel: Mapped[str] = mapped_column(String)   # sms, email, push, whatsapp
    status: Mapped[str] = mapped_column(String, default="pending")  # pending, sent, failed
    
    recipient: Mapped[str] = mapped_column(String)
    message: Mapped[str] = mapped_column(String)
    
    sent_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Alert(id={self.id}, severity={self.severity}, status={self.status})>"
