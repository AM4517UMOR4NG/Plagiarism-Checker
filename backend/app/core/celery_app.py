from celery import Celery
from app.config import settings

celery_app = Celery(
    "plagiarism_checker",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

# Optional: Json serialization
celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)
