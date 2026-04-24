from .celery_app import celery_app
from ..services.weather_service import WeatherService
from ..services.prediction_service import PredictionService
from ..ml.predict import get_prediction
from ..database import AsyncSessionLocal
from ..schemas.prediction import PredictionCreate
import uuid
import asyncio


async def run_prediction_task(weather_reading_id: str):
    """
    Main background task to run ML inference on a specific weather reading.
    """
    async with AsyncSessionLocal() as db:
        # 1. Fetch the weather reading
        # Note: In a real system we'd use the ID. For now we fetch latest as a fallback.
        reading = await WeatherService.get_latest_reading(db)
        if not reading:
            print("No weather reading found for prediction.")
            return

        # 2. Run ML model
        input_data = {
            "rainfall_mm": reading.rainfall_mm,
            "river_level_m": reading.river_level_m,
            "humidity_pct": reading.humidity_pct,
            "temperature_c": reading.temperature_c,
            "wind_speed_kmh": reading.wind_speed_kmh
        }
        
        prediction_result = get_prediction(input_data)
        
        if "error" in prediction_result:
            print(f"Prediction error: {prediction_result['error']}")
            return

        # 3. Store result
        prediction_in = PredictionCreate(
            weather_data_id=reading.id,
            risk_level=prediction_result["risk_level"],
            confidence=prediction_result["confidence"],
            model_version=prediction_result["model_version"]
        )
        
        db_prediction = await PredictionService.create_prediction(db, prediction_in)
        print(f"Prediction stored: Risk={db_prediction.risk_level} Confidence={db_prediction.confidence}")
        
        # 4. Trigger alert logic if risk level is above threshold
        if db_prediction.risk_level in ["Medium", "High", "Critical"]:
            celery_app.send_task("app.tasks.send_alerts.alert_dispatch_job", args=[str(db_prediction.id)])


@celery_app.task(name="app.tasks.run_predictions.prediction_job")
def prediction_job(weather_reading_id: str):
    """Celery wrapper for the prediction task."""
    loop = asyncio.get_event_loop()
    if loop.is_running():
        asyncio.create_task(run_prediction_task(weather_reading_id))
    else:
        loop.run_until_complete(run_prediction_task(weather_reading_id))
