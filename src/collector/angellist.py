"""AngelList API client."""

import logging
from typing import List, Optional
from datetime import datetime, timedelta

from src.models import Investor, Startup

logger = logging.getLogger(__name__)


class AngelListClient:
    """Client for AngelList API."""

    def __init__(self, access_token: str = None):
        self.access_token = access_token
        self.base_url = "https://api.angel.co/1"
        # Mock data for demo
        self.mock_startups = [
            {
                "id": "startup_al_001",
                "name": "InnovateTech",
                "industry": "AI",
                "stage": "seed",
                "description": "AI-powered workflow automation platform",
                "funding_needed": 1500000,
                "location": "Austin, TX",
                "website": "https://innovatetech.com",
                "founders": ["Sarah Connor", "John Reese"],
            },
            {
                "id": "startup_al_002",
                "name": "CloudBase",
                "industry": "SaaS",
                "stage": "series-a",
                "description": "Enterprise cloud management solution",
                "funding_needed": 5000000,
                "location": "Denver, CO",
                "website": "https://cloudbase.io",
                "founders": ["Mike Ross"],
            },
        ]

    def get_funding_announcements(self) -> List[dict]:
        """Fetch funding updates from AngelList."""
        logger.info("Fetching funding announcements from AngelList")

        if not self.access_token:
            logger.info("Using mock AngelList data (no access token)")
            mock_announcements = [
                {
                    "id": "ann_001",
                    "company_id": "startup_al_001",
                    "company_name": "InnovateTech",
                    "industry": "AI",
                    "stage": "seed",
                    "amount": 1500000,
                    "date": (datetime.now() - timedelta(days=2)).isoformat(),
                    "investor_ids": ["inv_al_001"],
                },
                {
                    "id": "ann_002",
                    "company_name": "CloudBase",
                    "industry": "SaaS",
                    "stage": "series-a",
                    "amount": 5000000,
                    "date": (datetime.now() - timedelta(days=6)).isoformat(),
                    "investor_ids": ["inv_al_002"],
                },
            ]
            return mock_announcements

        # TODO: Implement real API call
        logger.warning("Real AngelList API integration not yet implemented")
        return []

    def search_investors(self, criteria: dict) -> List[Investor]:
        """Search for investors by criteria."""
        logger.info(f"Searching investors with criteria: {criteria}")

        if not self.access_token:
            # Return mock investors that match basic criteria
            mock_investors = [
                Investor(
                    id="inv_al_001",
                    name="Sarah Kim",
                    email="sarah@futurefund.com",
                    firm="Future Fund",
                    focus_areas=["AI", "ML", "Deep Tech"],
                    stage_preference=["seed", "pre-seed"],
                    portfolio=["InnovateTech", "DataLabs"],
                    recent_investments=["2025-03-01: DataLabs - Seed - $2M"],
                    connections=[],
                    location="San Francisco, CA",
                    check_size_min=250000,
                    check_size_max=3000000,
                    website="https://futurefund.com",
                ),
                Investor(
                    id="inv_al_002",
                    name="David Chen",
                    email="david@scalevc.com",
                    firm="Scale VC",
                    focus_areas=["SaaS", "Enterprise", "B2B"],
                    stage_preference=["series-a", "series-b"],
                    portfolio=["CloudBase", "EnterpriseX"],
                    recent_investments=["2025-02-20: EnterpriseX - Series A - $12M"],
                    connections=["Reed Hastings"],
                    location="New York, NY",
                    check_size_min=3000000,
                    check_size_max=15000000,
                    website="https://scalevc.com",
                ),
            ]

            # Simple filtering based on criteria
            filtered = []
            for inv in mock_investors:
                match = True
                if "industry" in criteria:
                    if criteria["industry"].lower() not in [
                        area.lower() for area in inv.focus_areas
                    ]:
                        match = False
                if "stage" in criteria:
                    if criteria["stage"] not in inv.stage_preference:
                        match = False
                if match:
                    filtered.append(inv)
            return filtered

        # TODO: Implement real API call
        logger.warning("Real AngelList API integration not yet implemented")
        return []
