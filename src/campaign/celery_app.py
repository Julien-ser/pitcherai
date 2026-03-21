"""Celery configuration for PitcheRai."""

from celery import Celery
from src.config import settings

app = Celery(
    "pitcherai",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=[
        "src.campaign.tasks",
    ],
)

app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=29 * 60,  # 29 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

app.conf.task_routes = {
    "src.campaign.tasks.collect_funding_data": {"queue": "collectors"},
    "src.campaign.tasks.discover_and_draft": {"queue": "processing"},
    "src.campaign.tasks.send_campaign_emails": {"queue": "sending"},
    "src.campaign.tasks.check_responses": {"queue": "processing"},
    "src.campaign.tasks.update_learning": {"queue": "processing"},
}
