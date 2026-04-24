from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings


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

# CORS configuration
origins = settings.CORS_ORIGINS.split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health_check():
    """Health check endpoint to verify system status."""
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "version": "1.0.0"
    }


# Router registration
app.include_router(weather.router, prefix="/api/weather", tags=["Weather"])
app.include_router(predictions.router, prefix="/api/predictions", tags=["Predictions"])
app.include_router(alerts.router, prefix="/api/alerts", tags=["Alerts"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
