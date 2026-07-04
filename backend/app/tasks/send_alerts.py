from .celery_app import celery_app
from ..services.prediction_service import PredictionService
from ..services.alert_service import AlertService
from ..services.user_service import UserService
from ..database import AsyncSessionLocal, engine
from ..schemas.alert import AlertCreate
import asyncio
import uuid
import logging
from datetime import datetime, timezone, timedelta

logger = logging.getLogger(__name__)

# Deduplication window: don't send same severity alert to same user within this period
DEDUP_WINDOW_MINUTES = 30


async def alert_dispatch_task(prediction_id: str):
    """
    Background task to dispatch multi-channel alerts to all registered users.
    Includes deduplication to prevent alert spam.
    """
    async with AsyncSessionLocal() as db:
        # 1. Fetch prediction by specific ID
        prediction = await PredictionService.get_prediction_by_id(db, uuid.UUID(prediction_id))
        if not prediction:
            logger.warning(f"Prediction {prediction_id} not found, using latest.")
            prediction = await PredictionService.get_latest_prediction(db)
            if not prediction:
                logger.error("No prediction found for alert dispatch.")
                return

        # 2. Fetch all active users
        users = await UserService.get_all_active_users(db)
        if not users:
            logger.info("No active users registered for alerts.")
            return

        # 3. Check deduplication: get recent alerts within window
        cutoff = datetime.now(timezone.utc) - timedelta(minutes=DEDUP_WINDOW_MINUTES)
        recent_alerts = await AlertService.get_recent_alerts_since(db, cutoff)
        recent_recipients = {
            (a.recipient, a.severity) for a in recent_alerts
        }

        # 4. Create alert records and dispatch notifications
        dispatched = 0
        skipped = 0
        for user in users:
            # Deduplication check
            if (user.email, prediction.risk_level) in recent_recipients:
                logger.info(f"Dedup: Skipping {user.email} (already alerted for {prediction.risk_level})")
                skipped += 1
                continue

            message = (
                f"⚠️ FLOOD ALERT — {prediction.risk_level} Risk\n"
                f"Location: Otuoke, Bayelsa State\n"
                f"Risk Score: {prediction.risk_score:.0%}\n"
                f"Confidence: {prediction.confidence:.0%}\n"
                f"Time: {datetime.now(timezone.utc).strftime('%H:%M %d/%m/%Y')} UTC\n"
                f"Please take precautionary measures immediately."
            )

            # Create record in DB
            alert_in = AlertCreate(
                prediction_id=prediction.id,
                severity=prediction.risk_level,
                channel="multi",  # SuprSend handles multi-channel dispatch
                recipient=user.email,
                message=message
            )

            db_alert = await AlertService.create_alert_record(db, alert_in)

            # Dispatch via SuprSend (simulated service call)
            await AlertService.trigger_notification(db_alert)
            dispatched += 1

            logger.info(f"Alert dispatched to {user.name} ({user.email})")

        logger.info(f"Alert dispatch complete: {dispatched} sent, {skipped} deduplicated")


@celery_app.task(name="app.tasks.send_alerts.alert_dispatch_job", bind=True, max_retries=3)
def alert_dispatch_job(self, prediction_id: str):
    """Celery wrapper for the alert dispatch task with retry logic."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(alert_dispatch_task(prediction_id))
    except Exception as exc:
        logger.error(f"Alert dispatch failed: {exc}")
        self.retry(exc=exc, countdown=60)
    finally:
        try:
            loop.run_until_complete(engine.dispose())
        except Exception as e:
            logger.error(f"Error disposing engine pool: {e}")
        loop.close()
