import sys
import os
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

# Add current directory to path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app.database import Base, engine
# Import all models to register them on Base.metadata
from app.models.weather import WeatherData
from app.models.prediction import Prediction
from app.models.alert import Alert
from app.models.user import User

async def init_models():
    print("Connecting to database and creating tables...")
    async with engine.begin() as conn:
        # Drop all tables first if you want a clean slate (optional, commented out)
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created successfully!")

if __name__ == "__main__":
    asyncio.run(init_models())
