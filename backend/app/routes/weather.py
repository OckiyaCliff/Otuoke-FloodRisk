from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..database import get_db
from ..schemas.weather import WeatherData, WeatherDataCreate
from ..services.weather_service import WeatherService

router = APIRouter()


@router.post("/", response_model=WeatherData)
async def create_weather_data(
    weather_in: WeatherDataCreate, 
    db: AsyncSession = Depends(get_db)
):
    """Submit a new weather data point."""
    return await WeatherService.create_weather_reading(db, weather_in)


@router.get("/latest", response_model=WeatherData)
async def get_latest_weather(db: AsyncSession = Depends(get_db)):
    """Retrieve the most recent weather reading."""
    reading = await WeatherService.get_latest_reading(db)
    if not reading:
        raise HTTPException(status_code=404, detail="No weather data found")
    return reading


@router.get("/", response_model=List[WeatherData])
async def get_weather_history(
    limit: int = 50, 
    db: AsyncSession = Depends(get_db)
):
    """Retrieve a list of recent weather readings."""
    return await WeatherService.get_recent_readings(db, limit)
