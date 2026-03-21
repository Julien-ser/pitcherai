"""AngelList collector client."""

import requests
from typing import List, Dict, Any, Optional
from .base import BaseCollector
from src.config import settings


class AngelListClient(BaseCollector):
    """Client for AngelList API."""

    BASE_URL = "https://api.angel.co/1"

    def __init__(self, access_token: Optional[str] = None):
        self.access_token = access_token or settings.angellist_access_token
        self.session = requests.Session()
        if self.access_token:
            self.session.headers["Authorization"] = f"Bearer {self.access_token}"

    def get_recent_funding_announcements(self) -> List[Dict[str, Any]]:
        """Get funding announcements from AngelList."""
        if not self.access_token:
            return []

        try:
            response = self.session.get(
                f"{self.BASE_URL}/startup_fundings",
                params={"per_page": 100},
                timeout=30,
            )

            if response.status_code == 200:
                data = response.json()
                return self._parse_fundings(data)
            return []
        except Exception:
            return []

    def _parse_fundings(self, data: Dict) -> List[Dict[str, Any]]:
        """Parse funding data."""
        announcements = []
        for funding in data.get("fundings", []):
            try:
                announcement = {
                    "id": str(funding.get("id")),
                    "source": "angellist",
                    "company_name": funding.get("startup", {}).get("name", ""),
                    "company_url": funding.get("startup", {}).get("angellist_url", ""),
                    "funding_amount": funding.get("amount"),
                    "funding_round": funding.get("round"),
                    "announcement_date": funding.get("published_at"),
                    "investors": self._extract_investor_ids(funding),
                    "industry": funding.get("startup", {})
                    .get("markets", [{}])[0]
                    .get("name", "")
                    if funding.get("startup", {}).get("markets")
                    else "",
                    "stage": self._map_round_to_stage(funding.get("round")),
                }
                announcements.append(announcement)
            except Exception:
                continue
        return announcements

    def _extract_investor_ids(self, funding: Dict) -> List[str]:
        """Extract investor IDs."""
        investors = []
        for inv in funding.get("investors", []):
            investors.append(str(inv.get("id")))
        return investors

    def _map_round_to_stage(self, round_type: str) -> str:
        """Map funding round to stage."""
        if not round_type:
            return "seed"
        round_lower = round_type.lower()
        if "seed" in round_lower:
            return "seed"
        elif "angel" in round_lower:
            return "pre-seed"
        elif "series a" in round_lower:
            return "series-a"
        elif "series b" in round_lower:
            return "series-b"
        return "seed"

    def get_investor_details(self, investor_id: str) -> Optional[Dict[str, Any]]:
        """Get investor details from AngelList."""
        if not self.access_token or not investor_id:
            return None

        try:
            response = self.session.get(
                f"{self.BASE_URL}/users/{investor_id}",
                timeout=30,
            )

            if response.status_code == 200:
                data = response.json()
                return self._parse_investor(data)
            return None
        except Exception:
            return None

    def _parse_investor(self, data: Dict) -> Dict[str, Any]:
        """Parse investor data."""
        return {
            "id": str(data.get("id")),
            "name": data.get("name", ""),
            "firm": data.get("company_name", data.get("name", "")),
            "email": data.get("email", ""),
            "title": data.get("bio", "")[:100] if data.get("bio") else "",
            "bio": data.get("bio", ""),
            "industry_focus": self._extract_interests(data),
            "investment_stage": ["seed", "series-a"],  # Default
            "website": data.get("website", ""),
            "linkedin_url": data.get("linkedin_url", ""),
            "location": data.get("location", {}).get("name", "")
            if data.get("location")
            else "",
        }

    def _extract_interests(self, data: Dict) -> List[str]:
        """Extract investment interests."""
        interests = []
        for interest in data.get("interests", []):
            if interest.get("name"):
                interests.append(interest["name"])
        return interests[:10]

    def search_investors(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search for investors."""
        # Simplified - in production use AngelList search
        return []

    def get_recent_funding_rounds(self, days_back: int = 7) -> List[Dict[str, Any]]:
        """Get recent funding rounds (compatibility with BaseCollector)."""
        # AngelList API doesn't directly support date-filtered funding rounds
        # Use existing method which returns recent announcements
        return self.get_recent_funding_announcements()
