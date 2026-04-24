from pydantic import BaseModel, ConfigDict
from datetime import datetime
import uuid
from typing import Optional


class AlertBase(BaseModel):
    prediction_id: uuid.UUID
    severity: str
    channel: str
    recipient: str
    message: str


class AlertCreate(AlertBase):
    pass


class Alert(AlertBase):
    id: uuid.UUID
    status: str
    sent_at: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
