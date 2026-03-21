"""PitcheRai Orchestrator - ties all modules together."""

import asyncio
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime

from src.config import settings
from src.database import (
    init_db,
    get_engine,
    investors,
    startups,
    campaigns,
    email_templates,
    outreaches,
)
from src.models_db import InvestorDB, StartupDB, CampaignDB, EmailTemplateDB, OutreachDB
from src.models import Investor, Startup, Campaign, EmailTemplate, Outreach
from src.collector import CrunchbaseClient, AngelListClient, RSSCollector
from src.targeter import TargetFilter, TargetRanker, ConnectionFinder
from src.drafter import Personalizer, LLMClient
from src.campaign import CampaignManager, Scheduler, EmailSender, ResponseTracker
from src.email import GmailClient

logger = logging.getLogger(__name__)


class PitcheRaiOrchestrator:
    """Main orchestrator for PitcheRai system."""

    def __init__(self):
        self.db_engine = None
        self.db_session = None
        self.campaign_manager = CampaignManager()
        self.scheduler = Scheduler(rate_limit=settings.email_rate_limit)
        self.gmail_client = GmailClient()
        self.email_sender = EmailSender(self.gmail_client, settings.email_rate_limit)
        self.response_tracker = ResponseTracker(self.gmail_client)
        self.personalizer = Personalizer()
        self.llm_client = LLMClient(
            api_key=settings.openrouter_api_key, model=settings.default_model
        )
        self.collectors = {
            "crunchbase": CrunchbaseClient(settings.crunchbase_api_key),
            "angellist": AngelListClient(settings.angellist_access_token),
            "rss": RSSCollector(),
        }
        self.ranker = TargetRanker()
        self.connection_finder = ConnectionFinder()

    async def initialize(self):
        """Initialize database and external services."""
        logger.info("Initializing PitcheRai orchestrator...")

        # Initialize database
        self.db_engine = get_engine(settings.database_url)
        init_db(self.db_engine)
        from sqlalchemy.orm import sessionmaker

        self.db_session = sessionmaker(
            bind=self.db_engine, autocommit=False, autoflush=False
        )()
        logger.info("Database initialized")

        # Authenticate Gmail if credentials available
        if settings.gmail_client_id and settings.gmail_client_secret:
            # This would need proper OAuth flow - for now just log
            logger.info("Gmail credentials found - authentication required via API")

        logger.info("Orchestrator initialized successfully")

    def shutdown(self):
        """Cleanup resources."""
        if self.db_session:
            self.db_session.close()
        logger.info("Orchestrator shutdown complete")

    # ========== Data Collection ==========

    async def collect_funding_announcements(
        self, source: str = "all", days_back: int = 7
    ) -> List[Dict]:
        """Collect funding announcements from specified source(s)."""
        announcements = []

        sources = [source] if source != "all" else list(self.collectors.keys())

        for src in sources:
            if src not in self.collectors:
                logger.warning(f"Unknown collector: {src}")
                continue

            collector = self.collectors[src]
            try:
                if src == "crunchbase":
                    results = collector.get_recent_funding_rounds(days_back)
                elif src == "angellist":
                    results = collector.get_funding_announcements()
                elif src == "rss":
                    results = await collector.parse_feeds(days_back)
                else:
                    results = []

                announcements.extend(results)
                logger.info(f"Collected {len(results)} announcements from {src}")
            except Exception as e:
                logger.error(f"Error collecting from {src}: {e}")

        return announcements

    async def discover_investors(
        self, startup: Startup, days_back: int = 30
    ) -> List[Investor]:
        """Discover and rank investors based on startup profile."""
        logger.info(
            f"Discovering investors for {startup.name} ({startup.industry}, {startup.stage})"
        )

        # Step 1: Collect raw funding data
        announcements = await self.collect_funding_announcements(days_back=days_back)

        # Step 2: Extract investor IDs from announcements
        investor_ids = set()
        for ann in announcements:
            # Extract from different sources
            if "investors" in ann:
                investor_ids.update(ann["investors"])
            elif "investor_ids" in ann:
                investor_ids.update(ann["investor_ids"])

        logger.info(f"Found {len(investor_ids)} unique investor IDs from announcements")

        # Step 3: Fetch detailed investor information
        investors_list = []
        for inv_id in investor_ids:
            # Try each collector to find investor details
            for collector_name, collector in self.collectors.items():
                try:
                    if hasattr(collector, "get_investor_details"):
                        investor = collector.get_investor_details(inv_id)
                        if investor:
                            investors_list.append(investor)
                            break
                except Exception as e:
                    logger.debug(
                        f"Collector {collector_name} could not fetch {inv_id}: {e}"
                    )

        # If no investors from IDs, use search to find matching investors
        if not investors_list:
            logger.info("No investors found by ID, searching by criteria instead")
            criteria = {
                "industry": startup.industry,
                "stage": startup.stage,
            }
            for collector in self.collectors.values():
                if hasattr(collector, "search_investors"):
                    try:
                        results = collector.search_investors(criteria)
                        investors_list.extend(results)
                    except Exception as e:
                        logger.debug(f"Search failed: {e}")

        logger.info(f"Discovered {len(investors_list)} investors total")
        return investors_list

    def filter_and_rank_investors(
        self, startup: Startup, investors: List[Investor]
    ) -> List[Investor]:
        """Filter investors by relevance and rank by score."""
        logger.info(f"Filtering and ranking {len(investors)} investors")

        # Step 1: Apply filters
        filter_engine = TargetFilter(startup)
        filtered = filter_engine.filter(investors)
        logger.info(f"After filtering: {len(filtered)} investors remain")

        # Step 2: Rank by relevance
        ranked_pairs = self.ranker.rank_investors(filtered, startup)
        ranked_investors = [inv for inv, score in ranked_pairs]

        # Log top 10 with scores
        for i, (inv, score) in enumerate(ranked_pairs[:10]):
            logger.info(f"Rank {i + 1}: {inv.name} at {inv.firm} (score: {score:.1f})")

        return ranked_investors

    # ========== Campaign Management ==========

    def create_campaign_from_startup(
        self,
        startup: Startup,
        investors: List[Investor],
        name: str = None,
        target_criteria: Dict = None,
    ) -> Campaign:
        """Create a campaign with drafted emails for each investor."""
        campaign_name = (
            name
            or f"Campaign for {startup.name} - {datetime.utcnow().strftime('%Y-%m-%d')}"
        )

        # Create campaign
        campaign = self.campaign_manager.create_campaign(
            startup=startup, target_criteria=target_criteria or {}, name=campaign_name
        )

        # Add targets
        self.campaign_manager.add_targets(campaign.id, investors)

        # Generate drafted emails (in draft status)
        self._draft_campaign_emails(campaign, startup, investors)

        logger.info(f"Created campaign {campaign.id} with {len(investors)} targets")
        return campaign

    def _draft_campaign_emails(
        self, campaign: Campaign, startup: Startup, investors: List[Investor]
    ):
        """Draft personalized emails for all investors in campaign."""
        logger.info("Drafting personalized emails...")

        # Use the best template variant for each investor based on connections
        for investor in investors:
            try:
                # Choose template variant
                variant = "warm_intro" if investor.connections else "cold_pitch"

                # Draft email (this is simplified - should use LLM)
                email_template = self.personalizer.draft_email(
                    startup=startup,
                    investor=investor,
                    template_variant=variant,
                    founder_name="Founder",  # TODO: Get from startup data
                    founder_email=startup.email or "founder@example.com",
                )

                # Create outreach record
                outreach = Outreach(
                    id=f"out_{campaign.id}_{investor.id}",
                    campaign_id=campaign.id,
                    investor_id=investor.id,
                    template_id=email_template.id,
                    subject=email_template.subject,
                    body=email_template.body,
                    status="draft",
                )

                # Save to database (TODO: actually persist)
                logger.debug(f"Drafted email for {investor.name}: {outreach.subject}")

            except Exception as e:
                logger.error(f"Failed to draft email for {investor.name}: {e}")

        logger.info("Email drafting completed")

    # ========== Email Sending ==========

    async def send_campaign_emails(
        self, campaign_id: str, batch_size: int = 10
    ) -> Dict:
        """Send queued emails for a campaign."""
        logger.info(f"Starting email send for campaign {campaign_id}")

        # Get campaign
        if campaign_id not in self.campaign_manager.campaigns:
            raise ValueError(f"Campaign {campaign_id} not found")

        campaign = self.campaign_manager.campaigns[campaign_id]

        # Get all outreaches for campaign that are in draft status
        # TODO: Query database instead
        outreaches = []  # Placeholder

        # Queue them for sending
        for outreach in outreaches:
            self.email_sender.queue_email(outreach)

        # Process queue
        result = await self.email_sender.process_queue(self.db_session)

        logger.info(f"Campaign {campaign_id} send completed: {result}")
        return result

    async def check_and_update_responses(self):
        """Check for email responses and update statuses."""
        logger.info("Checking for email responses...")

        # Get all sent outreaches that don't have responses yet
        # TODO: Query from database properly
        outreaches = []

        # Check replies
        replies = await self.response_tracker.track_all_responses(self.db_session)

        # Update each outreach
        for outreach in outreaches:
            # Find matching reply
            for reply in replies:
                if outreach.id in reply.get("snippet", ""):
                    updated = await self.response_tracker.update_outreach_status(
                        outreach, reply["snippet"]
                    )
                    # Save to database
                    logger.info(
                        f"Updated outreach {outreach.id} with response: {updated.response_type}"
                    )

        logger.info(f"Response check completed: {len(replies)} replies found")
        return replies

    # ========== Learning ==========

    def update_campaign_learning(self, campaign_id: str):
        """Update learning models based on campaign performance."""
        logger.info(f"Updating learning for campaign {campaign_id}")

        # Get campaign metrics
        metrics = self.campaign_manager.get_campaign_metrics(campaign_id)

        # Update template scores (simple version)
        # TODO: Implement more sophisticated learning
        logger.info(f"Metrics: {metrics}")

        return metrics

    # ========== Dashboard Data ==========

    def get_dashboard_overview(self) -> Dict[str, Any]:
        """Get metrics for dashboard overview."""
        all_campaigns = list(self.campaign_manager.campaigns.values())

        active_campaigns = [c for c in all_campaigns if c.status == "active"]
        completed_campaigns = [c for c in all_campaigns if c.status == "completed"]

        # Calculate totals (would come from DB in real implementation)
        total_outreaches = sum(len(c.targets) for c in all_campaigns)

        return {
            "total_campaigns": len(all_campaigns),
            "active_campaigns": len(active_campaigns),
            "completed_campaigns": len(completed_campaigns),
            "total_outreaches": total_outreaches,
            "total_sent": 0,  # TODO: Query DB
            "total_opened": 0,
            "total_replied": 0,
        }

    def get_investor_list(self, search: str = None, limit: int = 100) -> List[Dict]:
        """Get list of investors with optional search."""
        # This would query the database
        return []

    def get_campaign_details(self, campaign_id: str) -> Optional[Dict]:
        """Get full campaign details including metrics."""
        if campaign_id not in self.campaign_manager.campaigns:
            return None

        campaign = self.campaign_manager.campaigns[campaign_id]
        metrics = self.campaign_manager.get_campaign_metrics(campaign_id)

        # Get outreaches for campaign (would come from DB)
        outreaches = []

        return {
            "campaign": campaign.dict(),
            "metrics": metrics,
            "outreaches": [o.dict() for o in outreaches],
        }


# Global orchestrator instance
_orchestrator: Optional[PitcheRaiOrchestrator] = None


def get_orchestrator() -> PitcheRaiOrchestrator:
    """Get or create the global orchestrator instance."""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = PitcheRaiOrchestrator()
    return _orchestrator
