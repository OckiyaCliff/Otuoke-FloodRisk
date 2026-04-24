from celery import Celery
from ..config import settings

# Initialize Celery app
celery_app = Celery(
    "floodrisk",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=[
        "app.tasks.fetch_data",
        "app.tasks.run_predictions",
        "app.tasks.send_alerts"
    ]
)

# Celery configurations
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Africa/Lagos",
    enable_utc=True,
    beat_schedule={
        "fetch-weather-every-10-minutes": {
            "task": "app.tasks.fetch_data.fetch_weather_job",
            "schedule": 600.0,  # 10 minutes in seconds
        },
    }
)

if __name__ == "__main__":
    celery_app.start()
