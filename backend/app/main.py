from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import engine
from sqlalchemy import text
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


from .routes import weather, predictions, alerts, users

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic (e.g., DB connection check)
    print(f"Starting {settings.APP_NAME} in {settings.APP_ENV} mode...")
    yield
    # Shutdown logic
    print(f"Shutting down {settings.APP_NAME}...")


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    lifespan=lifespan,
)

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


from fastapi.responses import JSONResponse

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
        "version": "1.0.0"
    }


# Router registration
app.include_router(weather.router, prefix="/api/weather", tags=["Weather"])
app.include_router(predictions.router, prefix="/api/predictions", tags=["Predictions"])
app.include_router(alerts.router, prefix="/api/alerts", tags=["Alerts"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
