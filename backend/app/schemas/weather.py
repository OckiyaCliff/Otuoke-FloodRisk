from pydantic import BaseModel, ConfigDict
from datetime import datetime
import uuid
from typing import Optional


class WeatherDataBase(BaseModel):
    rainfall_mm: float
    river_level_m: float
    humidity_pct: float
    temperature_c: float
    wind_speed_kmh: float
    pressure_hpa: Optional[float] = None
    river_discharge_m3s: Optional[float] = None
    source: str = "open-meteo"


class WeatherDataCreate(WeatherDataBase):
    pass


class WeatherData(WeatherDataBase):
    id: uuid.UUID
    recorded_at: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
