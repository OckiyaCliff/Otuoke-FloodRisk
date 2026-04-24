from pydantic import BaseModel, ConfigDict
from datetime import datetime
import uuid


class PredictionBase(BaseModel):
    weather_data_id: uuid.UUID
    risk_level: str
    confidence: float
    model_version: str


class PredictionCreate(PredictionBase):
    pass


class Prediction(PredictionBase):
    id: uuid.UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
