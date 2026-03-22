"""Investor prospecting and data collection service."""

from typing import List, Dict, Any, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
import httpx
from .. import crud
from ..models import Investment
from ..schemas import InvestorCreate
from ..config import settings


class ProspectingService:
    """Service for discovering and importing investors from various sources."""

    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()

    async def fetch_crunchbase_investors(
        self, query: str, limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Fetch investors from Crunchbase API.
        Note: Requires Crunchbase API key in settings.
        """
        if not settings.crunchbase_api_key:
            print("Crunchbase API key not configured, skipping")
            return []

        try:
            response = await self.client.get(
                "https://api.crunchbase.com/v4/entities/organizations",
                params={
                    "query": query,
                    "types": "investors",
                    "limit": limit,
                },
                headers={"X-cb-user-key": settings.crunchbase_api_key},
            )
            response.raise_for_status()
            data = response.json()

            investors = []
            for entity in data.get("entities", {}).values():
                investor_data = self._parse_crunchbase_entity(entity)
                if investor_data:
                    investors.append(investor_data)

            return investors
        except Exception as e:
            print(f"Error fetching from Crunchbase: {e}")
            return []

    def _parse_crunchbase_entity(
        self, entity: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Parse Crunchbase entity into investor data."""
        try:
            properties = entity.get("properties", {})
            name = properties.get("name")
            if not name:
                return None
            return {
                "name": name,
                "investor_type": "vc",  # Default assumption
                "firm_name": name,
                "email": None,  # Crunchbase doesn't provide direct email
                "linkedin_url": properties.get("linkedin", {}).get("value"),
                "focus_areas": self._extract_focus_areas(properties),
                "location": properties.get("location_identifiers", [{}])[0].get("value")
                if properties.get("location_identifiers")
                else None,
                "source": "crunchbase",
                "raw_data": entity,
            }
        except Exception:
            return None

    def _extract_focus_areas(self, properties: Dict[str, Any]) -> List[str]:
        """Extract focus areas from category groups."""
        categories = properties.get("category_groups", [])
        return [cat.get("value", "") for cat in categories if cat.get("value")]

    async def fetch_angellist_investors(
        self, query: str, limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Fetch investors from AngelList API.
        Note: Requires AngelList API access token.
        """
        if not settings.angellist_access_token:
            print("AngelList access token not configured, skipping")
            return []

        try:
            response = await self.client.get(
                "https://api.angel.co/1/search",
                params={"query": query, "type": "investors", "per_page": limit},
                headers={"Authorization": f"Bearer {settings.angellist_access_token}"},
            )
            response.raise_for_status()
            data = response.json()

            investors = []
            for investor in data.get("investors", []):
                parsed = self._parse_angellist_investor(investor)
                if parsed:
                    investors.append(parsed)

            return investors
        except Exception as e:
            print(f"Error fetching from AngelList: {e}")
            return []

    def _parse_angellist_investor(
        self, investor: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Parse AngelList investor data."""
        try:
            name = investor.get("name")
            if not name:
                return None
            return {
                "name": name,
                "investor_type": "angel" if investor.get("type") == "angel" else "vc",
                "firm_name": investor.get("company", {}).get("name"),
                "email": investor.get("email"),
                "linkedin_url": investor.get("linkedin_url"),
                "focus_areas": investor.get("tags", []),
                "location": investor.get("location", {}).get("name"),
                "source": "angellist",
                "raw_data": investor,
            }
        except Exception:
            return None

    async def import_investors_from_sources(
        self,
        session: AsyncSession,
        queries: List[str],
        sources: List[str] = ["crunchbase", "angellist"],
        limit_per_source: int = 50,
    ) -> int:
        """
        Import investors from multiple sources based on queries.

        Args:
            session: Database session
            queries: List of search queries (e.g., ["AI", "SaaS", "FinTech"])
            sources: List of sources to fetch from
            limit_per_source: Max investors per source per query

        Returns:
            Total number of investors imported
        """
        total_imported = 0

        for query in queries:
            for source in sources:
                if source == "crunchbase":
                    investors = await self.fetch_crunchbase_investors(
                        query, limit_per_source
                    )
                elif source == "angellist":
                    investors = await self.fetch_angellist_investors(
                        query, limit_per_source
                    )
                else:
                    continue

                for investor_data in investors:
                    # Check if investor already exists
                    existing = await crud.investor.get_by_email(
                        session, email=investor_data.get("email") or ""
                    )
                    if not existing and investor_data.get("name"):
                        # Create new investor
                        create_schema = InvestorCreate(
                            name=investor_data["name"],
                            investor_type=investor_data["investor_type"],
                            firm_name=investor_data.get("firm_name"),
                            email=investor_data.get("email"),
                            linkedin_url=investor_data.get("linkedin_url"),
                            focus_areas=investor_data.get("focus_areas", []),
                            location=investor_data.get("location"),
                            source=investor_data["source"],
                            raw_data=investor_data.get("raw_data", {}),
                        )
                        await crud.investor.create(session, obj_in=create_schema)
                        total_imported += 1

        return total_imported

    async def enrich_investor_portfolio(
        self, session: AsyncSession, investor_id: UUID
    ) -> int:
        """
        Enrich an investor's portfolio with their recent investments.

        Args:
            session: Database session
            investor_id: UUID of the investor to enrich

        Returns:
            Number of investments added
        """
        investor = await crud.investor.get(session, id=investor_id)
        if not investor:
            return 0

        investments_added = 0

        # Try to fetch from Crunchbase if we have their entity ID
        if investor.raw_data and "crunchbase_id" in investor.raw_data:
            try:
                crunchbase_id = investor.raw_data["crunchbase_id"]
                response = await self.client.get(
                    f"https://api.crunchbase.com/v4/entities/organizations/{crunchbase_id}/investments",
                    headers={"X-cb-user-key": settings.crunchbase_api_key},
                )
                response.raise_for_status()
                data = response.json()

                for investment in data.get("entities", {}).values():
                    added = await self._add_investment_from_crunchbase(
                        session, investor_id, investment
                    )
                    if added:
                        investments_added += 1
            except Exception as e:
                print(f"Error fetching investments from Crunchbase: {e}")

        return investments_added

    async def _add_investment_from_crunchbase(
        self, session: AsyncSession, investor_id: UUID, investment_data: Dict[str, Any]
    ) -> bool:
        """Add an investment from Crunchbase data.

        Returns:
            True if investment was added, False otherwise.
        """
        try:
            props = investment_data.get("properties", {})
            startup_name = props.get("company_name", "")
            round_type = props.get("funding_type", "")

            if startup_name:
                # Check if investment already exists
                existing = await session.execute(
                    select(Investment).where(
                        and_(
                            Investment.investor_id == investor_id,
                            Investment.startup_name == startup_name,
                        )
                    )
                )
                if not existing.scalar_one_or_none():
                    # Parse the date string to a date object if provided
                    announced_date_str = props.get("announced_date")
                    investment_date = None
                    if announced_date_str:
                        try:
                            # Handle both date-only and datetime strings
                            from datetime import datetime

                            if "T" in announced_date_str:
                                # ISO datetime format
                                dt = datetime.fromisoformat(
                                    announced_date_str.replace("Z", "+00:00")
                                )
                                investment_date = dt.date()
                            else:
                                # Simple date format (YYYY-MM-DD)
                                investment_date = datetime.strptime(
                                    announced_date_str, "%Y-%m-%d"
                                ).date()
                        except (ValueError, TypeError):
                            investment_date = None

                    investment = Investment(
                        investor_id=investor_id,
                        startup_name=startup_name,
                        round_type=round_type,
                        investment_date=investment_date,
                        raw_data=investment_data,
                    )
                    session.add(investment)
                    await session.flush()
                    return True
            return False
        except Exception as e:
            print(f"Error adding investment: {e}")
            # Rollback to recover session state
            await session.rollback()
            return False


# Global instance
prospecting_service = ProspectingService()
