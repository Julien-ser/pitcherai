"""Crunchbase API client for funding data."""

from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


class CrunchbaseClient:
    """Client for Crunchbase API."""

    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_recent_funding_rounds(self, limit: int = 100) -> List[dict]:
        """Fetch recent funding announcements."""
        logger.info("Fetching funding rounds from Crunchbase")
        return []

    def get_investor_details(self, investor_id: str) -> Optional[dict]:
        """Get detailed investor information."""
        logger.info(f"Fetching investor: {investor_id}")
        return None
