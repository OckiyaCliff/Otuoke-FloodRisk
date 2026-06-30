from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc
from typing import List, Optional
import uuid
from ..models.weather import WeatherData
from ..schemas.weather import WeatherDataCreate


class WeatherService:
    @staticmethod
    async def create_weather_reading(db: AsyncSession, weather_in: WeatherDataCreate) -> WeatherData:
        """Create a new weather data record in the database."""
        db_weather = WeatherData(**weather_in.model_dump())
        db.add(db_weather)
        await db.commit()
        await db.refresh(db_weather)
        return db_weather

    @staticmethod
    async def get_reading_by_id(db: AsyncSession, reading_id: uuid.UUID) -> Optional[WeatherData]:
        """Fetch a specific weather reading by its UUID."""
        query = select(WeatherData).where(WeatherData.id == reading_id)
        result = await db.execute(query)
        return result.scalars().first()

    @staticmethod
    async def get_latest_reading(db: AsyncSession) -> Optional[WeatherData]:
        """Fetch the most recent weather reading."""
        query = select(WeatherData).order_by(desc(WeatherData.recorded_at)).limit(1)
        result = await db.execute(query)
        return result.scalars().first()

    @staticmethod
    async def get_recent_readings(db: AsyncSession, limit: int = 100) -> List[WeatherData]:
        """Fetch multiple recent weather readings."""
        query = select(WeatherData).order_by(desc(WeatherData.recorded_at)).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all())
