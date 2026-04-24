from .celery_app import celery_app
from ..services.prediction_service import PredictionService
from ..services.alert_service import AlertService
from ..services.user_service import UserService
from ..database import AsyncSessionLocal
from ..schemas.alert import AlertCreate
import asyncio
import uuid


async def alert_dispatch_task(prediction_id: str):
    """
    Background task to dispatch multi-channel alerts to all registered users.
    """
    async with AsyncSessionLocal() as db:
        # 1. Fetch prediction details
        # Fallback to latest for simulation
        prediction = await PredictionService.get_latest_prediction(db)
        if not prediction:
            print("No prediction found for alert dispatch.")
            return

        # 2. Fetch all active users
        users = await UserService.get_all_active_users(db)
        if not users:
            print("No active users registered for alerts.")
            return

        # 3. Create alert records and dispatch notifications
        for user in users:
            message = f"URGENT: {prediction.risk_level} Flood Risk detected at Otuoke. Rainfall: high, River Level: rising. Please stay alert."
            
            # Create record in DB
            alert_in = AlertCreate(
                prediction_id=prediction.id,
                severity=prediction.risk_level,
                channel="multi", # SuprSend handles the multi-channel dispatch
                recipient=user.email,
                message=message
            )
            
            db_alert = await AlertService.create_alert_record(db, alert_in)
            
            # Dispatch via SuprSend (simulated service call)
            await AlertService.trigger_notification(db_alert)
            
            print(f"Alert dispatched to {user.name} ({user.email})")


@celery_app.task(name="app.tasks.send_alerts.alert_dispatch_job")
def alert_dispatch_job(prediction_id: str):
    """Celery wrapper for the alert dispatch task."""
    loop = asyncio.get_event_loop()
    if loop.is_running():
        asyncio.create_task(alert_dispatch_task(prediction_id))
    else:
        loop.run_until_complete(alert_dispatch_task(prediction_id))
