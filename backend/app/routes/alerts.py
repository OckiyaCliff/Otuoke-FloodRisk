from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..database import get_db
from ..schemas.alert import Alert, AlertCreate
from ..services.alert_service import AlertService

router = APIRouter()


@router.post("/", response_model=Alert)
async def create_alert(
    alert_in: AlertCreate, 
    db: AsyncSession = Depends(get_db)
):
    """Manually create an alert (usually triggered by background tasks)."""
    return await AlertService.create_alert_record(db, alert_in)


@router.get("/", response_model=List[Alert])
async def get_alerts_history(
    limit: int = 50, 
    db: AsyncSession = Depends(get_db)
):
    """Retrieve historical flood alerts."""
    return await AlertService.get_alerts_history(db, limit)
