from datetime import datetime, timezone
import uuid
from sqlalchemy import Float, String, DateTime, UUID, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column
from ..database import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    weather_data_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("weather_data.id"))

    risk_level: Mapped[str] = mapped_column(String)  # No Risk, Low, Medium, High, Critical
    risk_score: Mapped[float] = mapped_column(Float, default=0.0)  # 0.0 - 1.0 numeric score
    confidence: Mapped[float] = mapped_column(Float)
    model_version: Mapped[str] = mapped_column(String)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Performance indexes
    __table_args__ = (
        Index("ix_predictions_created_at", "created_at"),
    )

    def __repr__(self) -> str:
        return f"<Prediction(id={self.id}, risk={self.risk_level}, score={self.risk_score}, confidence={self.confidence})>"
