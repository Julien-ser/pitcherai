"""Crunchbase collector client."""

import requests
from typing import List, Dict, Any
from .base import BaseCollector
from src.config import settings


class CrunchbaseClient(BaseCollector):
    """Client for Crunchbase API."""

    BASE_URL = "https://api.crunchbase.com/api/v4"

    def __init__(self, api_key: str = None):
        self.api_key = api_key or settings.crunchbase_api_key
        self.session = requests.Session()

    def get_recent_funding_rounds(self, days_back: int = 7) -> List[Dict[str, Any]]:
        """Get recent funding rounds."""
        if not self.api_key:
            return []

        try:
            from datetime import datetime, timedelta

            cutoff_date = datetime.utcnow() - timedelta(days=days_back)
            iso_date = cutoff_date.isoformat()

            response = self.session.get(
                f"{self.BASE_URL}/funding_rounds/search",
                params={
                    "query": f"announced_on:{iso_date}..*",
                    "page": 1,
                    "per_page": 100,
                },
                timeout=30,
            )

            if response.status_code == 200:
                data = response.json()
                return self._parse_funding_rounds(data.get("entities", []))
            else:
                return []
        except Exception as e:
            return []

    def _parse_funding_rounds(self, entities: List[Dict]) -> List[Dict[str, Any]]:
        """Parse funding round entities."""
        announcements = []
        for entity in entities:
            try:
                props = entity.get("properties", {})
                announcement = {
                    "id": entity.get("uuid"),
                    "source": "crunchbase",
                    "company_name": props.get("company_name"),
                    "company_url": props.get("company_url"),
                    "funding_amount": props.get("money_raised"),
                    "funding_round": props.get("funding_round_type"),
                    "announcement_date": props.get("announced_on"),
                    "investors": self._extract_investor_ids(entity),
                    "industry": self._extract_industry(entity),
                    "stage": self._map_round_to_stage(props.get("funding_round_type")),
                }
                announcements.append(announcement)
            except Exception:
                continue
        return announcements

    def _extract_investor_ids(self, entity: Dict) -> List[str]:
        """Extract investor IDs from entity."""
        investors = []
        for investor in entity.get("relationships", {}).get("investors", []):
            investors.append(investor.get("uuid"))
        return investors

    def _extract_industry(self, entity: Dict) -> str:
        """Extract industry from entity."""
        categories = entity.get("relationships", {}).get("category_groups", [])
        if categories:
            return categories[0].get("properties", {}).get("name", "")
        return ""

    def _map_round_to_stage(self, round_type: str) -> str:
        """Map funding round type to stage."""
        mapping = {
            "seed": "seed",
            "angel": "pre-seed",
            "pre-seed": "pre-seed",
            "series_a": "series-a",
            "series_b": "series-b",
            "series_c": "series-c",
        }
        return mapping.get(round_type.lower(), "seed")

    def get_investor_details(self, investor_id: str) -> Dict[str, Any]:
        """Get investor details from Crunchbase."""
        if not self.api_key or not investor_id:
            return None

        try:
            response = self.session.get(
                f"{self.BASE_URL}/organizations/{investor_id}",
                timeout=30,
            )

            if response.status_code == 200:
                data = response.json()
                return self._parse_investor(data)
            return None
        except Exception:
            return None

    def _parse_investor(self, data: Dict) -> Dict[str, Any]:
        """Parse investor entity."""
        props = data.get("properties", {})
        return {
            "id": data.get("uuid"),
            "name": props.get("name", ""),
            "firm": props.get("name", ""),
            "email": props.get("email", ""),
            "title": props.get("short_description", ""),
            "bio": props.get("long_description", ""),
            "industry_focus": self._extract_categories(data),
            "investment_stage": self._extract_investment_stages(data),
            "website": props.get("website", {}).get("url", ""),
            "linkedin_url": props.get("linkedin", {}).get("url", ""),
            "location": self._extract_location(data),
        }

    def _extract_categories(self, data: Dict) -> List[str]:
        """Extract investment categories."""
        categories = []
        for cat in data.get("relationships", {}).get("category_groups", []):
            cat_props = cat.get("properties", {})
            if cat_props.get("name"):
                categories.append(cat_props["name"])
        return categories

    def _extract_investment_stages(self, data: Dict) -> List[str]:
        """Extract investment stages."""
        stages = []
        for investment in data.get("relationships", {}).get("investments", []):
            inv_props = investment.get("properties", {})
            round_type = inv_props.get("funding_round_type", "")
            if round_type:
                mapped = self._map_round_to_stage(round_type)
                if mapped not in stages:
                    stages.append(mapped)
        return stages or ["seed", "series-a"]

    def _extract_location(self, data: Dict) -> str:
        """Extract location."""
        for loc in data.get("relationships", {}).get("locations", []):
            return loc.get("properties", {}).get("name", "")
        return ""

    def search_investors(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search for investors by criteria."""
        # Simplified implementation - in production would use Crunchbase search API
        return []
