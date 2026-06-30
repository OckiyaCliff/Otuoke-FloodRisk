from .celery_app import celery_app
from ..services.weather_service import WeatherService
from ..schemas.weather import WeatherDataCreate
from ..database import AsyncSessionLocal
from ..config import settings
import httpx
import asyncio
import logging

logger = logging.getLogger(__name__)


async def fetch_weather_task():
    """
    Fetch real-time weather data from Open-Meteo API for Otuoke.
    Falls back to the last known reading if the API is unavailable.
    """
    weather_data = None

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Fetch current weather
            weather_resp = await client.get(settings.OPENMETEO_WEATHER_URL, params={
                "latitude": settings.OTUOKE_LATITUDE,
                "longitude": settings.OTUOKE_LONGITUDE,
                "current": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m,surface_pressure",
                "timezone": "Africa/Lagos"
            })
            weather_resp.raise_for_status()
            weather_json = weather_resp.json()
            current = weather_json["current"]

            # Fetch river discharge
            river_discharge = 0.0
            try:
                flood_resp = await client.get(settings.OPENMETEO_FLOOD_URL, params={
                    "latitude": settings.OTUOKE_LATITUDE,
                    "longitude": settings.OTUOKE_LONGITUDE,
                    "daily": "river_discharge",
                    "past_days": 1,
                })
                flood_resp.raise_for_status()
                flood_json = flood_resp.json()
                discharges = flood_json.get("daily", {}).get("river_discharge", [])
                if discharges:
                    river_discharge = discharges[-1] or 0.0
            except Exception as e:
                logger.warning(f"Flood API unavailable, using 0 discharge: {e}")

            # Map to our schema
            rainfall = current.get("precipitation", 0.0) or 0.0
            river_level = max(0.3, river_discharge * 0.4 + 0.5)  # Approximate river level from discharge

            weather_data = WeatherDataCreate(
                rainfall_mm=rainfall,
                river_level_m=round(river_level, 2),
                humidity_pct=current.get("relative_humidity_2m", 70.0) or 70.0,
                temperature_c=current.get("temperature_2m", 28.0) or 28.0,
                wind_speed_kmh=current.get("wind_speed_10m", 5.0) or 5.0,
                pressure_hpa=current.get("surface_pressure", 1013.0) or 1013.0,
                river_discharge_m3s=river_discharge,
                source="open-meteo"
            )

            logger.info(f"Open-Meteo data fetched: rain={rainfall}mm, discharge={river_discharge}m³/s")

    except Exception as e:
        logger.error(f"Open-Meteo API error: {e}. Weather data not available this cycle.")
        return

    if weather_data is None:
        return

    async with AsyncSessionLocal() as db:
        reading = await WeatherService.create_weather_reading(db, weather_data)
        logger.info(f"Weather reading stored: ID={reading.id}")

        # Trigger prediction job asynchronously
        celery_app.send_task("app.tasks.run_predictions.prediction_job", args=[str(reading.id)])


@celery_app.task(name="app.tasks.fetch_data.fetch_weather_job")
def fetch_weather_job():
    """Wrapper to run the async task in Celery's synchronous environment."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(fetch_weather_task())
    finally:
        loop.close()
