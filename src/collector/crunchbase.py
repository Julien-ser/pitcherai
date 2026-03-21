"""Crunchbase API client for funding data."""

import logging
from typing import List, Optional
from datetime import datetime, timedelta

from src.models import Investor, Startup

logger = logging.getLogger(__name__)


class CrunchbaseClient:
    """Client for Crunchbase API."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.base_url = "https://api.crunchbase.com/v3"
        # Mock data for demo when API key not provided
        self.mock_investors = [
            {
                "id": "inv_cb_001",
                "name": "Alice Johnson",
                "email": "alice@aiventures.com",
                "firm": "AI Ventures",
                "focus_areas": ["AI", "Machine Learning", "LLMs"],
                "stage_preference": ["seed", "series-a"],
                "portfolio": ["DataFlow AI", "NeuralBot", "ChatEngine"],
                "recent_investments": ["2025-03-01: DataFlow AI - Series A - $15M"],
                "connections": ["John Smith (ex-Google)"],
                "location": "San Francisco, CA",
                "check_size_min": 500000,
                "check_size_max": 5000000,
                "website": "https://aiventures.com",
            },
            {
                "id": "inv_cb_002",
                "name": "Bob Martinez",
                "email": "bob@saasfund.com",
                "firm": "SaaS Fund",
                "focus_areas": ["SaaS", "B2B", "Productivity"],
                "stage_preference": ["series-a", "series-b"],
                "portfolio": ["TaskMaster", "CloudSync"],
                "recent_investments": ["2025-02-15: TaskMaster - Series B - $30M"],
                "connections": [],
                "location": "New York, NY",
                "check_size_min": 2000000,
                "check_size_max": 20000000,
                "website": "https://saasfund.com",
            },
        ]

    def get_recent_funding_rounds(self, days_back: int = 7) -> List[dict]:
        """Fetch recent funding announcements."""
        logger.info(f"Fetching funding rounds from Crunchbase (last {days_back} days)")

        if not self.api_key:
            # Return mock data
            logger.info("Using mock Crunchbase data (no API key)")
            mock_rounds = [
                {
                    "id": "round_001",
                    "company_name": "TechFlow Inc",
                    "industry": "AI",
                    "stage": "seed",
                    "amount": 2500000,
                    "date": (datetime.now() - timedelta(days=3)).isoformat(),
                    "investors": ["inv_cb_001"],
                },
                {
                    "id": "round_002",
                    "company_name": "CloudSync Pro",
                    "industry": "SaaS",
                    "stage": "series-a",
                    "amount": 8000000,
                    "date": (datetime.now() - timedelta(days=5)).isoformat(),
                    "investors": ["inv_cb_002"],
                },
            ]
            return mock_rounds

        # TODO: Implement real API call
        logger.warning("Real Crunchbase API integration not yet implemented")
        return []

    def get_investor_details(self, investor_id: str) -> Optional[Investor]:
        """Get detailed investor information."""
        logger.info(f"Fetching investor details: {investor_id}")

        if not self.api_key:
            # Return mock data if investor_id matches
            for inv_data in self.mock_investors:
                if inv_data["id"] == investor_id:
                    return Investor(**inv_data)
            return None

        # TODO: Implement real API call
        logger.warning("Real Crunchbase API integration not yet implemented")
        return None
