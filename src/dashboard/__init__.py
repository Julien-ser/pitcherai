"""Dashboard UI and API endpoints."""

from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from src.models import Campaign, Outreach, Investor
from src.campaign import CampaignManager
from src.email import GmailClient


# FastAPI app for backend
api_app = FastAPI(title="PitcheRai API", version="0.1.0")


class DashboardAPI:
    """Dashboard backend API."""

    def __init__(self, campaign_manager: CampaignManager, gmail_client: GmailClient):
        self.campaign_manager = campaign_manager
        self.gmail_client = gmail_client

    @api_app.get("/api/investors")
    async def list_investors(
        self, search: str = "", industry: str = "", limit: int = 100
    ) -> List[Dict[str, Any]]:
        """List and search investors."""
        raise NotImplementedError("Investors endpoint pending implementation")

    @api_app.get("/api/campaigns")
    async def list_campaigns(self, status: str = "") -> List[Dict[str, Any]]:
        """List campaigns."""
        raise NotImplementedError("Campaigns list endpoint pending implementation")

    @api_app.post("/api/campaigns")
    async def create_campaign(self, campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new campaign."""
        raise NotImplementedError("Campaign creation pending implementation")

    @api_app.get("/api/campaigns/{campaign_id}")
    async def get_campaign(self, campaign_id: str) -> Dict[str, Any]:
        """Get campaign details with metrics."""
        raise NotImplementedError("Campaign detail endpoint pending implementation")

    @api_app.put("/api/outreaches/{outreach_id}")
    async def override_outreach(
        self, outreach_id: str, updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Override email draft before sending."""
        raise NotImplementedError("Override endpoint pending implementation")

    @api_app.post("/api/outreaches/{outreach_id}/send")
    async def send_outreach(self, outreach_id: str) -> Dict[str, Any]:
        """Manually trigger send for an outreach."""
        raise NotImplementedError("Manual send endpoint pending implementation")

    @api_app.get("/api/metrics")
    async def get_metrics(self) -> Dict[str, Any]:
        """Dashboard metrics summary."""
        raise NotImplementedError("Metrics endpoint pending implementation")


class StreamlitDashboard:
    """Streamlit frontend dashboard."""

    def __init__(self, api_base_url: str = "http://localhost:8000"):
        self.api_base_url = api_base_url

    def run(self):
        """Run the Streamlit dashboard."""
        raise NotImplementedError("Streamlit dashboard pending implementation")

    def render_campaign_list(self):
        """Render campaign list view."""
        raise NotImplementedError("UI rendering pending implementation")

    def render_campaign_detail(self, campaign_id: str):
        """Render campaign detail view with outreach queue."""
        raise NotImplementedError("UI rendering pending implementation")

    def render_metrics_dashboard(self):
        """Render metrics and charts."""
        raise NotImplementedError("Metrics visualization pending implementation")
