"""Celery tasks for async processing."""

import asyncio
import logging
from typing import Dict, Any
from datetime import datetime

from src.orchestrator import get_orchestrator
from src.models import Startup

logger = logging.getLogger(__name__)

# Note: We're using asyncio in tasks, which requires some care with Celery
# In production you might want to use a different approach or ensure proper loop handling


# Task 1: Collect funding data from all sources
async def _collect_task(days_back: int = 7):
    """Internal async task for data collection."""
    orchestrator = get_orchestrator()
    await orchestrator.initialize()

    try:
        announcements = await orchestrator.collect_funding_announcements(
            days_back=days_back
        )
        return {
            "status": "completed",
            "announcements_found": len(announcements),
            "timestamp": datetime.utcnow().isoformat(),
        }
    finally:
        orchestrator.shutdown()


def collect_funding_data(days_back: int = 7):
    """Celery task: collect funding data from all sources."""
    return asyncio.run(_collect_task(days_back))


# Task 2: Discover investors and create campaign
async def _discover_draft_task(startup_data: Dict[str, Any], campaign_name: str):
    """Internal async task for investor discovery and campaign creation."""
    orchestrator = get_orchestrator()
    await orchestrator.initialize()

    try:
        # Create startup object
        startup = Startup(**startup_data)

        # Discover investors
        investors = await orchestrator.discover_investors(startup)

        # Filter and rank
        ranked = orchestrator.filter_and_rank_investors(startup, investors)

        # Create campaign with drafted emails
        campaign = orchestrator.create_campaign_from_startup(
            startup=startup,
            investors=ranked[:50],  # Limit to top 50
            name=campaign_name,
        )

        return {
            "status": "completed",
            "campaign_id": campaign.id,
            "investors_discovered": len(investors),
            "investors_filtered": len(ranked),
            "targets_added": len(campaign.targets),
            "timestamp": datetime.utcnow().isoformat(),
        }
    finally:
        orchestrator.shutdown()


def discover_and_draft(startup_data: Dict[str, Any], campaign_name: str):
    """Celery task: discover investors and draft campaign emails."""
    return asyncio.run(_discover_draft_task(startup_data, campaign_name))


# Task 3: Send campaign emails
async def _send_campaign_task(campaign_id: str, batch_size: int = 10):
    """Internal async task for sending campaign emails."""
    orchestrator = get_orchestrator()
    await orchestrator.initialize()

    try:
        result = await orchestrator.send_campaign_emails(campaign_id, batch_size)
        return {
            "status": "completed",
            "result": result,
            "timestamp": datetime.utcnow().isoformat(),
        }
    finally:
        orchestrator.shutdown()


def send_campaign_emails(campaign_id: str, batch_size: int = 10):
    """Celery task: send queued emails for a campaign."""
    return asyncio.run(_send_campaign_task(campaign_id, batch_size))


# Task 4: Check for responses
async def _check_responses_task():
    """Internal async task for checking responses."""
    orchestrator = get_orchestrator()
    await orchestrator.initialize()

    try:
        replies = await orchestrator.check_and_update_responses()
        return {
            "status": "completed",
            "replies_found": len(replies),
            "timestamp": datetime.utcnow().isoformat(),
        }
    finally:
        orchestrator.shutdown()


def check_responses():
    """Celery task: check for email responses."""
    return asyncio.run(_check_responses_task())


# Task 5: Update learning
async def _update_learning_task(campaign_id: str):
    """Celery task for updating learning models."""
    orchestrator = get_orchestrator()
    try:
        await orchestrator.initialize()
        metrics = orchestrator.update_campaign_learning(campaign_id)
        orchestrator.shutdown()
        return {
            "status": "completed",
            "metrics": metrics,
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        logger.error(f"Learning update failed for campaign {campaign_id}: {e}")
        orchestrator.shutdown()
        raise


def update_learning(campaign_id: str):
    """Celery task: update learning models based on campaign results."""
    return asyncio.run(_update_learning_task(campaign_id))
