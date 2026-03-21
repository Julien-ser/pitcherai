"""Campaign orchestration and management."""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
import time

from src.models import Campaign, EmailTemplate, Investor, Outreach, Startup
from src.database import db as database

logger = logging.getLogger(__name__)


class CampaignManager:
    """Manage outreach campaigns end-to-end."""

    def __init__(self):
        self.campaigns: dict[str, Campaign] = {}
        self.db = database

    def create_campaign(
        self, startup: Startup, target_criteria: dict[str, Any], name: str
    ) -> Campaign:
        """Create a new outreach campaign."""
        campaign_id = f"camp_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        campaign = Campaign(
            id=campaign_id,
            startup_id=startup.id,
            name=name,
            target_criteria=target_criteria,
            status="draft",
        )
        self.campaigns[campaign_id] = campaign
        logger.info(f"Created campaign: {campaign_id} - {name}")
        return campaign

    def add_targets(self, campaign_id: str, investors: list[Investor]):
        """Add target investors to campaign."""
        if campaign_id in self.campaigns:
            self.campaigns[campaign_id].targets = [inv.id for inv in investors]
            logger.info(f"Added {len(investors)} targets to campaign {campaign_id}")

    def start_campaign(self, campaign_id: str):
        """Activate a campaign."""
        if campaign_id in self.campaigns:
            self.campaigns[campaign_id].status = "active"
            self.campaigns[campaign_id].started_at = datetime.utcnow()
            logger.info(f"Started campaign: {campaign_id}")

    def pause_campaign(self, campaign_id: str):
        """Pause an active campaign."""
        if campaign_id in self.campaigns:
            self.campaigns[campaign_id].status = "paused"
            logger.info(f"Paused campaign: {campaign_id}")

    def complete_campaign(self, campaign_id: str):
        """Mark campaign as completed."""
        if campaign_id in self.campaigns:
            self.campaigns[campaign_id].status = "completed"
            self.campaigns[campaign_id].completed_at = datetime.utcnow()
            logger.info(f"Completed campaign: {campaign_id}")

    def get_campaign_metrics(self, campaign_id: str) -> dict[str, Any]:
        """Calculate campaign metrics."""
        if campaign_id not in self.campaigns:
            return {}

        campaign = self.campaigns[campaign_id]
        outreaches = campaign.targets  # This would normally query DB

        # Basic metrics (would be calculated from actual outreaches in DB)
        metrics = {
            "total_targets": len(outreaches),
            "emails_sent": 0,
            "emails_opened": 0,
            "replies_received": 0,
            "positive_replies": 0,
            "open_rate": 0.0,
            "reply_rate": 0.0,
            "campaign_id": campaign_id,
            "status": campaign.status,
        }
        return metrics


class Scheduler:
    """Schedule email sends respecting rate limits."""

    def __init__(self, rate_limit: int = 10):
        self.rate_limit = rate_limit  # emails per minute
        self.queue: list[Outreach] = []
        self.last_send_times: list[float] = []

    def schedule_outreach(self, outreach: Outreach):
        """Add outreach to send queue."""
        self.queue.append(outreach)

    def schedule_batch(self, outreaches: list[Outreach]):
        """Add multiple outreaches to queue."""
        self.queue.extend(outreaches)

    def get_next_batch(self, batch_size: int) -> list[Outreach]:
        """Get next batch of emails to send."""
        batch = self.queue[:batch_size]
        self.queue = self.queue[batch_size:]
        return batch

    def should_wait(self) -> tuple[bool, float]:
        """Check if we need to wait for rate limit. Returns (should_wait, seconds)."""
        if not self.last_send_times:
            return False, 0.0

        # Keep only last minute's sends
        now = time.time()
        recent_sends = [t for t in self.last_send_times if now - t < 60]

        if len(recent_sends) >= self.rate_limit:
            # Need to wait until oldest send falls out of the window
            oldest = min(recent_sends)
            wait_seconds = 60 - (now - oldest)
            return True, max(0.0, wait_seconds)

        return False, 0.0

    def record_send(self):
        """Record that an email was sent."""
        self.last_send_times.append(time.time())
        # Clean up old entries
        now = time.time()
        self.last_send_times = [t for t in self.last_send_times if now - t < 60]

    def queue_size(self) -> int:
        """Get current queue size."""
        return len(self.queue)


class MetricsTracker:
    """Track campaign performance metrics."""

    def __init__(self):
        self.db = database

    def record_send(self, outreach_id: str):
        """Record that an email was sent."""
        # TODO: Update outreach status in DB
        logger.debug(f"Recorded send for outreach {outreach_id}")

    def record_open(self, outreach_id: str):
        """Record email open."""
        # TODO: Update outreach with open tracking
        logger.debug(f"Recorded open for outreach {outreach_id}")

    def record_reply(self, outreach_id: str, response_type: str):
        """Record a reply and its type."""
        # TODO: Update outreach with reply info
        logger.debug(
            f"Recorded reply for outreach {outreach_id}, type: {response_type}"
        )

    def get_campaign_stats(self, campaign_id: str) -> Dict[str, Any]:
        """Get statistics for a campaign."""
        # TODO: Query database for actual stats
        # For now return mock metrics
        return {
            "campaign_id": campaign_id,
            "total_sent": 0,
            "total_opened": 0,
            "total_replied": 0,
            "open_rate": 0.0,
            "reply_rate": 0.0,
            "positive_reply_rate": 0.0,
        }

    def get_dashboard_metrics(self) -> Dict[str, Any]:
        """Get overall dashboard metrics."""
        # TODO: Aggregate across all campaigns
        return {
            "total_campaigns": 0,
            "active_campaigns": 0,
            "total_outreaches": 0,
            "emails_sent": 0,
            "emails_opened": 0,
            "replies_received": 0,
        }


class LearningEngine:
    """Learn which templates and targets convert best."""

    def __init__(self):
        self.db = database

    def update_template_scores(self, campaign_id: str):
        """Update performance scores for templates based on results."""
        # TODO: Implement learning algorithm
        # For now, simple scoring based on reply rates
        logger.info(f"Updating template scores for campaign {campaign_id}")

    def predict_best_template(
        self, investor: Investor, startup: Startup
    ) -> EmailTemplate:
        """Predict best template for given investor-startup pair."""
        # TODO: Implement ML-based prediction
        # For now, return first available template
        from src.drafter import TemplateEngine

        engine = TemplateEngine()
        template = engine.get_template_by_variant("cold_pitch")
        if template:
            return template
        # Fallback
        return EmailTemplate(
            id="tpl_default",
            name="Default Template",
            subject=f"{startup.name} - Investment Opportunity",
            body=f"Dear {investor.name},\n\nWe are {startup.name}...",
            variant="cold_pitch",
        )
