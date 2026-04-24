from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..database import get_db
from ..schemas.prediction import Prediction, PredictionCreate
from ..services.prediction_service import PredictionService

from ..schemas.weather import WeatherDataBase
from ..ml.predict import get_prediction

router = APIRouter()


@router.post("/", response_model=Prediction)
async def create_prediction(
    prediction_in: PredictionCreate, 
    db: AsyncSession = Depends(get_db)
):
    """Record a new flood risk prediction manually."""
    return await PredictionService.create_prediction(db, prediction_in)


@router.post("/realtime", response_model=Prediction)
async def predict_realtime(
    weather_in: WeatherDataBase, 
    db: AsyncSession = Depends(get_db)
):
    """
    Accept real-time weather data, run ML prediction, and store result.
    """
    # 1. Store the weather data first (or simulate having an ID)
    # For now, we'll run prediction on the inputs directly
    prediction_result = get_prediction(weather_in.model_dump())
    
    if "error" in prediction_result:
        raise HTTPException(status_code=500, detail=prediction_result["error"])
        
    # 2. Store prediction
    # Note: In a real flow, we'd link to a WeatherData ID. 
    # For this endpoint, we'll use a dummy ID or make it optional.
    prediction_data = PredictionCreate(
        weather_data_id=uuid.uuid4(), # Placeholder till linked
        risk_level=prediction_result["risk_level"],
        confidence=prediction_result["confidence"],
        model_version=prediction_result["model_version"]
    )
    
    return await PredictionService.create_prediction(db, prediction_data)


@router.get("/latest", response_model=Prediction)
async def get_latest_prediction(db: AsyncSession = Depends(get_db)):
    """Retrieve the most recent prediction."""
    prediction = await PredictionService.get_latest_prediction(db)
    if not prediction:
        raise HTTPException(status_code=404, detail="No predictions found")
    return prediction


@router.get("/", response_model=List[Prediction])
async def get_predictions_history(
    limit: int = 50, 
    db: AsyncSession = Depends(get_db)
):
    """Retrieve historical flood risk predictions."""
    return await PredictionService.get_predictions_history(db, limit)
