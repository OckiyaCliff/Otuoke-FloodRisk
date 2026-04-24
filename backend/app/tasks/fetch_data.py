from .celery_app import celery_app
from ..services.weather_service import WeatherService
from ..schemas.weather import WeatherDataCreate
from ..database import AsyncSessionLocal
import random
import asyncio


async def fetch_weather_task():
    """
    Simulated weather data fetching task.
    In production, this would call an external meteorological API.
    """
    # Simulate weather reading
    weather_in = WeatherDataCreate(
        rainfall_mm=random.uniform(0, 120),
        river_level_m=random.uniform(0.5, 4.5),
        humidity_pct=random.uniform(50, 95),
        temperature_c=random.uniform(25, 33),
        wind_speed_kmh=random.uniform(0, 25),
        source="automated_sensor"
    )

    async with AsyncSessionLocal() as db:
        reading = await WeatherService.create_weather_reading(db, weather_in)
        print(f"Periodic weather fetch successful: ID {reading.id}")
        
        # Trigger prediction job asynchronously
        celery_app.send_task("app.tasks.run_predictions.prediction_job", args=[str(reading.id)])


@celery_app.task(name="app.tasks.fetch_data.fetch_weather_job")
def fetch_weather_job():
    """Wrapper to run the async task in Celery's synchronous environment."""
    loop = asyncio.get_event_loop()
    if loop.is_running():
        # This shouldn't typically happen in a Celery worker, but safety first
        asyncio.create_task(fetch_weather_task())
    else:
        loop.run_until_complete(fetch_weather_task())
