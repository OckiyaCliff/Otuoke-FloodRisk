from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
import uuid
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate


class UserService:
    @staticmethod
    async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
        """Register a new user for flood alerts."""
        db_user = User(**user_in.model_dump())
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
        """Fetch a user by email address."""
        query = select(User).where(User.email == email)
        result = await db.execute(query)
        return result.scalars().first()

    @staticmethod
    async def get_all_active_users(db: AsyncSession) -> List[User]:
        """Fetch all active users for alert broadcasting."""
        query = select(User).where(User.is_active == True)
        result = await db.execute(query)
        return list(result.scalars().all())
