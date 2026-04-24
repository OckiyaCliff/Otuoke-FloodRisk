from datetime import datetime
import uuid
from sqlalchemy import Float, String, DateTime, UUID
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
    
    source: Mapped[str] = mapped_column(String, default="simulated")
    recorded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<WeatherData(id={self.id}, rainfall={self.rainfall_mm}, river={self.river_level_m})>"
