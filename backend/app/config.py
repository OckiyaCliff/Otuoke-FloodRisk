from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://floodrisk:floodrisk_dev@localhost:5432/floodrisk"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # SuprSend
    SUPRSEND_WORKSPACE_KEY: str = ""
    SUPRSEND_WORKSPACE_SECRET: str = ""

    # App
    APP_NAME: str = "FUO Flood Early-Warning System"
    APP_ENV: str = "development"
    DEBUG: bool = True
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    # Alert Thresholds
    ALERT_THRESHOLD_LOW: float = 0.4
    ALERT_THRESHOLD_MEDIUM: float = 0.6
    ALERT_THRESHOLD_HIGH: float = 0.8

    # External Weather API (optional, for production)
    WEATHER_API_KEY: Optional[str] = None
    WEATHER_API_URL: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
