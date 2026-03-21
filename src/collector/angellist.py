"""AngelList API client."""

from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


class AngelListClient:
    """Client for AngelList API."""

    def __init__(self, access_token: str):
        self.access_token = access_token

    def get_funding_announcements(self) -> List[dict]:
        """Fetch funding updates from AngelList."""
        logger.info("Fetching from AngelList")
        return []

    def search_investors(self, criteria: dict) -> List[dict]:
        """Search for investors by criteria."""
        logger.info(f"Searching investors: {criteria}")
        return []
