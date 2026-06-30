from datetime import datetime, timezone
import uuid
from sqlalchemy import Float, String, DateTime, UUID, Index
from sqlalchemy.orm import Mapped, mapped_column
from ..database import Base


class WeatherData(Base):
    __tablename__ = "weather_data"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    rainfall_mm: Mapped[float] = mapped_column(Float)
    river_level_m: Mapped[float] = mapped_column(Float)
    humidity_pct: Mapped[float] = mapped_column(Float)
    temperature_c: Mapped[float] = mapped_column(Float)
    wind_speed_kmh: Mapped[float] = mapped_column(Float)

    # New fields for real-world data
    pressure_hpa: Mapped[float | None] = mapped_column(Float, nullable=True)
    river_discharge_m3s: Mapped[float | None] = mapped_column(Float, nullable=True)

    source: Mapped[str] = mapped_column(String, default="open-meteo")
    recorded_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    # Performance indexes
    __table_args__ = (
        Index("ix_weather_data_recorded_at", "recorded_at"),
    )

    def __repr__(self) -> str:
        return f"<WeatherData(id={self.id}, rainfall={self.rainfall_mm}, river={self.river_level_m}, discharge={self.river_discharge_m3s})>"
