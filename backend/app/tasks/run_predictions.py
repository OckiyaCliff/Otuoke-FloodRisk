from .celery_app import celery_app
from ..services.weather_service import WeatherService
from ..services.prediction_service import PredictionService
from ..ml.predict import get_prediction
from ..database import AsyncSessionLocal, engine
from ..schemas.prediction import PredictionCreate
import uuid
import asyncio
import logging

logger = logging.getLogger(__name__)


async def run_prediction_task(weather_reading_id: str):
    """
    Run ML inference on a specific weather reading by its ID.
    """
    async with AsyncSessionLocal() as db:
        # 1. Fetch the specific weather reading by ID
        reading = await WeatherService.get_reading_by_id(db, uuid.UUID(weather_reading_id))
        if not reading:
            # Fallback to latest reading if ID not found
            logger.warning(f"Weather reading {weather_reading_id} not found, using latest.")
            reading = await WeatherService.get_latest_reading(db)
            if not reading:
                logger.error("No weather reading found for prediction.")
                return

        # 2. Run ML model with all available features
        input_data = {
            "rainfall_mm": reading.rainfall_mm,
            "river_level_m": reading.river_level_m,
            "humidity_pct": reading.humidity_pct,
            "temperature_c": reading.temperature_c,
            "wind_speed_kmh": reading.wind_speed_kmh,
            "pressure_hpa": reading.pressure_hpa or 1013.25,
            "river_discharge_m3s": reading.river_discharge_m3s or 0.0,
        }

        prediction_result = get_prediction(input_data)

        if "error" in prediction_result:
            logger.error(f"Prediction error: {prediction_result['error']}")
            return

        # 3. Store result
        prediction_in = PredictionCreate(
            weather_data_id=reading.id,
            risk_level=prediction_result["risk_level"],
            risk_score=prediction_result.get("risk_score", 0.0),
            confidence=prediction_result["confidence"],
            model_version=prediction_result["model_version"]
        )

        db_prediction = await PredictionService.create_prediction(db, prediction_in)
        logger.info(
            f"Prediction stored: Risk={db_prediction.risk_level} "
            f"Score={db_prediction.risk_score} "
            f"Confidence={db_prediction.confidence}"
        )

        # 4. Trigger alert logic if risk level is above threshold
        if db_prediction.risk_level in ["Medium", "High", "Critical"]:
            celery_app.send_task(
                "app.tasks.send_alerts.alert_dispatch_job",
                args=[str(db_prediction.id)]
            )


@celery_app.task(name="app.tasks.run_predictions.prediction_job", bind=True, max_retries=3)
def prediction_job(self, weather_reading_id: str):
    """Celery wrapper for the prediction task with retry logic."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(run_prediction_task(weather_reading_id))
    except Exception as exc:
        logger.error(f"Prediction task failed: {exc}")
        self.retry(exc=exc, countdown=30)
    finally:
        try:
            loop.run_until_complete(engine.dispose())
        except Exception as e:
            logger.error(f"Error disposing engine pool: {e}")
        loop.close()
