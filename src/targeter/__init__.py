"""Investor filtering and ranking module."""

from typing import List, Tuple
import logging

from src.models import Investor, Startup

logger = logging.getLogger(__name__)


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
        # Simple keyword matching in portfolio/company names
        filtered = []
        startup_industry = self.startup.industry.lower()
        for inv in investors:
            has_competitor = False
            for portfolio_company in inv.portfolio:
                # Very simple: check if industry keywords appear in company name
                if startup_industry in portfolio_company.lower():
                    has_competitor = True
                    logger.debug(
                        f"Investor {inv.name} has portfolio company {portfolio_company} in same space"
                    )
                    break
            if not has_competitor:
                filtered.append(inv)
        return filtered

    def filter(self, investors: List[Investor]) -> List[Investor]:
        """Apply all filters."""
        filtered = self.filter_by_stage(investors)
        logger.info(f"After stage filter: {len(filtered)} investors")
        filtered = self.filter_by_industry(filtered)
        logger.info(f"After industry filter: {len(filtered)} investors")
        filtered = self.exclude_competitors(filtered)
        logger.info(f"After competitor exclusion: {len(filtered)} investors")
        return filtered


class TargetRanker:
    """Rank filtered investors by relevance."""

    def rank_investors(
        self, investors: List[Investor], startup: Startup
    ) -> List[Tuple[Investor, float]]:
        """Score and sort investors by conversion likelihood. Returns list of (investor, score)."""
        scored_investors = []
        for inv in investors:
            score = self._calculate_score(inv, startup)
            scored_investors.append((inv, score))

        # Sort by score descending
        scored_investors.sort(key=lambda x: x[1], reverse=True)
        return scored_investors

    def _calculate_score(self, investor: Investor, startup: Startup) -> float:
        """Calculate relevance score (0-100)."""
        score = 50.0  # Base score

        # Industry match gets +20 if exact match
        if startup.industry.lower() in [area.lower() for area in investor.focus_areas]:
            score += 20

        # Stage match gets +15 if exact match
        if startup.stage in investor.stage_preference:
            score += 15

        # Recent investments (-5 per recent investment, they might be oversubscribed)
        if investor.recent_investments:
            score -= min(len(investor.recent_investments) * 5, 20)

        # Shared connections (+10 per connection)
        if investor.connections:
            score += min(len(investor.connections) * 10, 30)

        # Location preference (+5 if same location or remote-friendly)
        if startup.location and investor.location:
            if startup.location.lower() == investor.location.lower():
                score += 5
            elif (
                "remote" in investor.location.lower()
                or "global" in investor.location.lower()
            ):
                score += 3

        # Check size preference (+5 if startup's funding need falls in investor's range)
        if (
            startup.funding_needed
            and investor.check_size_min
            and investor.check_size_max
        ):
            if (
                investor.check_size_min
                <= startup.funding_needed
                <= investor.check_size_max
            ):
                score += 5

        # Clamp score to 0-100
        score = max(0, min(100, score))
        return score


class ConnectionFinder:
    """Find shared connections via LinkedIn or other sources."""

    def find_connections(self, founder_email: str, investor: Investor) -> List[str]:
        """Find shared connections between founder and investor."""
        # Simple implementation: check if founder's domain matches investor portfolio company domains
        # In a real implementation, this would use LinkedIn API or similar
        connections = []

        # For now, return the investor's connections as-is (these would come from LinkedIn API)
        # In production, you'd call LinkedIn API to find mutual connections
        if investor.connections:
            connections.extend(investor.connections)

        return connections

    def find_connections_batch(
        self, founder_emails: List[str], investors: List[Investor]
    ) -> dict:
        """Find connections for multiple founders/investors."""
        results = {}
        for founder_email in founder_emails:
            for inv in investors:
                key = f"{founder_email}:{inv.id}"
                results[key] = self.find_connections(founder_email, inv)
        return results
