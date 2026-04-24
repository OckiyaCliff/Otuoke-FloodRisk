from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from .config import settings

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True if settings.APP_ENV == "development" else False,
)

# Async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""
    pass


async def get_db():
    """Dependency for getting async database sessions."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
