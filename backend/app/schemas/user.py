from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
import uuid
from typing import Dict


class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    preferences: Dict = {"notifications": {"email": True, "sms": True, "push": True}}


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    preferences: Optional[Dict] = None


class User(UserBase):
    id: uuid.UUID
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
