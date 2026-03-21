"""Dashboard UI and API endpoints."""

import logging
import uuid
from fastapi import FastAPI, HTTPException, Query
from typing import Any, Dict, List, Optional

from src.models import Startup
from src.campaign import CampaignManager, MetricsTracker
from src.collector import CrunchbaseCollector, AngelListCollector, RSSFeedCollector
from src.config import settings

logger = logging.getLogger(__name__)

# FastAPI app
api_app = FastAPI(title="PitcheRai API", version="0.1.0")

# Service instances
campaign_manager = CampaignManager()
metrics_tracker = MetricsTracker()

# Collectors (using settings for API keys, pass empty string if None)
crunchbase_collector = CrunchbaseCollector(api_key=settings.crunchbase_api_key or "")
angellist_collector = AngelListCollector(
    access_token=settings.angellist_access_token or ""
)
rss_collector = RSSFeedCollector()


@api_app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}


@api_app.get("/api/investors")
async def list_investors(
    search: str = Query("", description="Search term for name or firm"),
    industry: str = Query("", description="Filter by industry"),
    limit: int = Query(100, ge=1, le=1000),
) -> List[Dict[str, Any]]:
    """List investors, with optional search and filters."""
    # TODO: Implement database query with filters
    # For now, return empty list
    return []


@api_app.post("/api/campaigns")
async def create_campaign(
    startup_id: str, name: str, target_criteria: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Create a new outreach campaign."""
    try:
        if target_criteria is None:
            target_criteria = {}

        # For demo, create a dummy startup if not found in DB
        startup = Startup(
            id=startup_id,
            name="Demo Startup",
            industry="Tech",
            stage="seed",
            description="A demo startup",
            funding_needed=1000000,
        )

        campaign = campaign_manager.create_campaign(startup, target_criteria, name)
        logger.info(f"Created campaign: {campaign.id} - {name}")
        return campaign.dict()
    except Exception as e:
        logger.error(f"Failed to create campaign: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@api_app.get("/api/campaigns")
async def list_campaigns(
    status: Optional[str] = Query(None, description="Filter by status"),
) -> List[Dict[str, Any]]:
    """List all campaigns."""
    campaigns = list(campaign_manager.campaigns.values())
    if status:
        campaigns = [c for c in campaigns if c.status == status]
    return [c.dict() for c in campaigns]


@api_app.get("/api/campaigns/{campaign_id}")
async def get_campaign(campaign_id: str) -> Dict[str, Any]:
    """Get campaign details with metrics."""
    if campaign_id not in campaign_manager.campaigns:
        raise HTTPException(status_code=404, detail="Campaign not found")

    campaign = campaign_manager.campaigns[campaign_id]
    metrics = campaign_manager.get_campaign_metrics(campaign_id)

    return {
        "campaign": campaign.dict(),
        "metrics": metrics,
    }


@api_app.post("/api/campaigns/{campaign_id}/start")
async def start_campaign(campaign_id: str) -> Dict[str, Any]:
    """Start a campaign."""
    if campaign_id not in campaign_manager.campaigns:
        raise HTTPException(status_code=404, detail="Campaign not found")

    campaign_manager.start_campaign(campaign_id)
    logger.info(f"Started campaign: {campaign_id}")
    return {"status": "started", "campaign_id": campaign_id}


@api_app.post("/api/campaigns/{campaign_id}/pause")
async def pause_campaign(campaign_id: str) -> Dict[str, Any]:
    """Pause a campaign."""
    if campaign_id not in campaign_manager.campaigns:
        raise HTTPException(status_code=404, detail="Campaign not found")

    campaign_manager.pause_campaign(campaign_id)
    logger.info(f"Paused campaign: {campaign_id}")
    return {"status": "paused", "campaign_id": campaign_id}


@api_app.post("/api/campaigns/{campaign_id}/complete")
async def complete_campaign(campaign_id: str) -> Dict[str, Any]:
    """Mark campaign as completed."""
    if campaign_id not in campaign_manager.campaigns:
        raise HTTPException(status_code=404, detail="Campaign not found")

    campaign_manager.complete_campaign(campaign_id)
    logger.info(f"Completed campaign: {campaign_id}")
    return {"status": "completed", "campaign_id": campaign_id}


@api_app.get("/api/outreaches")
async def list_outreaches(
    campaign_id: Optional[str] = Query(None), status: Optional[str] = Query(None)
) -> List[Dict[str, Any]]:
    """List outreaches with optional filters."""
    # TODO: Query database with filters
    return []


@api_app.put("/api/outreaches/{outreach_id}")
async def override_outreach(
    outreach_id: str, updates: Dict[str, Any]
) -> Dict[str, Any]:
    """Override email draft before sending."""
    # TODO: Update outreach in database
    logger.info(f"Override outreach {outreach_id} with updates: {updates}")
    return {"status": "updated", "outreach_id": outreach_id}


@api_app.post("/api/outreaches/{outreach_id}/send")
async def send_outreach(outreach_id: str) -> Dict[str, Any]:
    """Manually trigger send for an outreach."""
    # TODO: Queue outreach for sending
    logger.info(f"Queued outreach for sending: {outreach_id}")
    return {"status": "queued", "outreach_id": outreach_id}


@api_app.get("/api/metrics")
async def get_metrics() -> Dict[str, Any]:
    """Get overall dashboard metrics."""
    metrics = metrics_tracker.get_dashboard_metrics()
    return metrics


@api_app.post("/api/collectors/rss")
async def collect_rss_feed() -> Dict[str, Any]:
    """Trigger RSS feed collection."""
    try:
        announcements = await rss_collector.parse_feeds(days_back=7)
        # TODO: Process announcements, extract companies/investors, save to database
        logger.info(f"RSS collection found {len(announcements)} announcements")
        return {
            "status": "completed",
            "announcements_found": len(announcements),
            "message": "RSS collection completed",
        }
    except Exception as e:
        logger.error(f"RSS collection failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@api_app.post("/api/collectors/crunchbase")
async def collect_crunchbase() -> Dict[str, Any]:
    """Trigger Crunchbase data collection."""
    try:
        fundings = await crunchbase_collector.fetch_recent_fundings()
        logger.info(f"Crunchbase collection found {len(fundings)} fundings")
        return {
            "status": "completed",
            "fundings_found": len(fundings),
            "message": "Crunchbase collection completed",
        }
    except Exception as e:
        logger.error(f"Crunchbase collection failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@api_app.post("/api/collectors/angellist")
async def collect_angellist() -> Dict[str, Any]:
    """Trigger AngelList data collection."""
    try:
        startups = await angellist_collector.fetch_startups()
        logger.info(f"AngelList collection found {len(startups)} startups")
        return {
            "status": "completed",
            "startups_found": len(startups),
            "message": "AngelList collection completed",
        }
    except Exception as e:
        logger.error(f"AngelList collection failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
