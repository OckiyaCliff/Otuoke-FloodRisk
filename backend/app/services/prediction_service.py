from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc
from typing import List, Optional
import uuid
from ..models.prediction import Prediction
from ..schemas.prediction import PredictionCreate


class PredictionService:
    @staticmethod
    async def create_prediction(db: AsyncSession, prediction_in: PredictionCreate) -> Prediction:
        """Store a new prediction in the database."""
        db_prediction = Prediction(**prediction_in.model_dump())
        db.add(db_prediction)
        await db.commit()
        await db.refresh(db_prediction)
        return db_prediction

    @staticmethod
    async def get_latest_prediction(db: AsyncSession) -> Optional[Prediction]:
        """Fetch the most recent flood risk prediction."""
        query = select(Prediction).order_by(desc(Prediction.created_at)).limit(1)
        result = await db.execute(query)
        return result.scalars().first()

    @staticmethod
    async def get_predictions_history(db: AsyncSession, limit: int = 50) -> List[Prediction]:
        """Fetch historical predictions."""
        query = select(Prediction).order_by(desc(Prediction.created_at)).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all())
