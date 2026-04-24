from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc
from typing import List, Optional
import uuid
from ..models.alert import Alert
from ..schemas.alert import AlertCreate
from ..config import settings
# from suprsend import Suprsend  # Will be used in the service logic


class AlertService:
    @staticmethod
    async def create_alert_record(db: AsyncSession, alert_in: AlertCreate) -> Alert:
        """Create a new alert record in the database."""
        db_alert = Alert(**alert_in.model_dump())
        db.add(db_alert)
        await db.commit()
        await db.refresh(db_alert)
        return db_alert

    @staticmethod
    async def get_alerts_history(db: AsyncSession, limit: int = 50) -> List[Alert]:
        """Fetch historical alerts."""
        query = select(Alert).order_by(desc(Alert.created_at)).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def trigger_notification(alert: Alert):
        """
        Trigger a notification event via SuprSend.
        In a real implementation, this would call the SuprSend SDK.
        """
        # Example SuprSend logic:
        # supr_client = Suprsend(settings.SUPRSEND_WORKSPACE_KEY, settings.SUPRSEND_WORKSPACE_SECRET)
        # supr_client.trigger_workflow({
        #     "event": "FLOOD_ALERT",
        #     "distinct_id": alert.recipient,
        #     "properties": {
        #         "severity": alert.severity,
        #         "message": alert.message
        #     }
        # })
        print(f"NOTIFICATION TRIGGERED: {alert.severity} to {alert.recipient} - {alert.message}")
        pass
