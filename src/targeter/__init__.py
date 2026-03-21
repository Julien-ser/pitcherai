"""Investor filtering and ranking module."""

from typing import List
from src.models import Investor, Startup


class TargetFilter:
    """Filter investors based on startup profile."""

    def __init__(self, startup: Startup):
        self.startup = startup

    def filter_by_stage(self, investors: List[Investor]) -> List[Investor]:
        """Filter investors by preferred funding stage."""
        return [inv for inv in investors if self.startup.stage in inv.stage_preference]

    def filter_by_industry(self, investors: List[Investor]) -> List[Investor]:
        """Filter investors by focus areas matching startup industry."""
        return [
            inv
            for inv in investors
            if self.startup.industry.lower()
            in [area.lower() for area in inv.focus_areas]
        ]

    def exclude_competitors(self, investors: List[Investor]) -> List[Investor]:
        """Exclude investors with portfolio companies in same space."""
        # Simple text matching - to be enhanced
        return investors

    def filter(self, investors: List[Investor]) -> List[Investor]:
        """Apply all filters."""
        filtered = self.filter_by_stage(investors)
        filtered = self.filter_by_industry(filtered)
        filtered = self.exclude_competitors(filtered)
        return filtered


class TargetRanker:
    """Rank filtered investors by relevance."""

    def rank_investors(
        self, investors: List[Investor], startup: Startup
    ) -> List[Investor]:
        """Score and sort investors by conversion likelihood."""
        raise NotImplementedError("Ranking algorithm pending implementation")


class ConnectionFinder:
    """Find shared connections via LinkedIn or other sources."""

    def find_connections(self, founder_email: str, investor: Investor) -> List[str]:
        """Find shared connections between founder and investor."""
        raise NotImplementedError("Connection finding pending implementation")
