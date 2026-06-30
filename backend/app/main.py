from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .config import settings
from .database import engine
from sqlalchemy import text
import logging

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

from .routes import weather, predictions, alerts, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown lifecycle."""
    logger.info(f"Starting {settings.APP_NAME} in {settings.APP_ENV} mode...")
    logger.info(f"Otuoke coordinates: ({settings.OTUOKE_LATITUDE}, {settings.OTUOKE_LONGITUDE})")
    yield
    logger.info(f"Shutting down {settings.APP_NAME}...")


app = FastAPI(
    title=settings.APP_NAME,
    version="2.0.0",
    description="Flood early-warning system for Federal University Otuoke, Bayelsa State. "
                "Powered by Open-Meteo real-time data and Random Forest ML predictions.",
    lifespan=lifespan,
)

# CORS configuration
origins = [o.strip() for o in settings.CORS_ORIGINS.split(",")]
if settings.APP_ENV == "development":
    dev_origins = ["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:8000"]
    for o in dev_origins:
        if o not in origins:
            origins.append(o)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error", "error": str(exc)},
    )


@app.get("/api/health")
async def health_check():
    """Enhanced health check with DB connectivity test."""
    db_status = "unknown"
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
            db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
        logger.error(f"Database health check failed: {e}")

    return {
        "status": "ok" if "error" not in db_status else "degraded",
        "database": db_status,
        "environment": settings.APP_ENV,
        "version": "2.0.0",
        "data_source": "Open-Meteo API",
        "location": {
            "name": "Otuoke, Bayelsa State",
            "lat": settings.OTUOKE_LATITUDE,
            "lon": settings.OTUOKE_LONGITUDE
        }
    }


# Router registration
app.include_router(weather.router, prefix="/api/weather", tags=["Weather"])
app.include_router(predictions.router, prefix="/api/predictions", tags=["Predictions"])
app.include_router(alerts.router, prefix="/api/alerts", tags=["Alerts"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
