from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..database import get_db
from ..schemas.user import User, UserCreate
from ..services.user_service import UserService

router = APIRouter()


@router.post("/", response_model=User)
async def register_user(
    user_in: UserCreate, 
    db: AsyncSession = Depends(get_db)
):
    """Register a new user to receive flood alerts."""
    existing_user = await UserService.get_user_by_email(db, user_in.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await UserService.create_user(db, user_in)


@router.get("/", response_model=List[User])
async def list_users(db: AsyncSession = Depends(get_db)):
    """Retrieve a list of all registered users."""
    return await UserService.get_all_active_users(db)
