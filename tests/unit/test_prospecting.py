"""Tests for Prospecting service."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from pitcherai.services.prospecting import ProspectingService
from pitcherai import crud
from pitcherai.schemas import InvestorCreate
from pitcherai.models import Investor


class TestProspectingService:
    """Tests for ProspectingService."""

    @pytest.fixture
    def prospecting_service(self):
        """Create a fresh service instance."""
        return ProspectingService()

    async def test_fetch_crunchbase_investors_no_api_key(
        self, prospecting_service: ProspectingService
    ):
        """Test that Crunchbase fetch returns empty when no API key."""
        from pitcherai.config import get_get_settings()

        # Temporarily clear the API key
        original_key = get_settings().crunchbase_api_key
        get_settings().crunchbase_api_key = None

        result = await prospecting_service.fetch_crunchbase_investors(
            query="AI", limit=10
        )

        assert result == []
        get_settings().crunchbase_api_key = original_key

    async def test_fetch_crunchbase_investors_success(
        self, prospecting_service: ProspectingService
    ):
        """Test successful Crunchbase fetch with mocked response."""
        from pitcherai.config import get_get_settings()

        # Ensure API key is set
        if not get_settings().crunchbase_api_key:
            pytest.skip("Crunchbase API key not configured")

        # Mock the httpx client
        prospecting_service.client = AsyncMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "entities": {
                "org123": {
                    "properties": {
                        "name": "AI Ventures",
                        "linkedin": {
                            "value": "https://linkedin.com/company/aiventures"
                        },
                        "location_identifiers": [{"value": "San Francisco"}],
                        "category_groups": [{"value": "Artificial Intelligence"}],
                    }
                }
            }
        }
        mock_response.raise_for_status = MagicMock()
        prospecting_service.client.get.return_value = mock_response

        result = await prospecting_service.fetch_crunchbase_investors(
            query="AI", limit=10
        )

        assert len(result) == 1
        assert result[0]["name"] == "AI Ventures"
        assert result[0]["source"] == "crunchbase"

    def test_parse_crunchbase_entity_valid(
        self, prospecting_service: ProspectingService
    ):
        """Test parsing a valid Crunchbase entity."""
        entity = {
            "properties": {
                "name": "Test VC",
                "linkedin": {"value": "https://linkedin.com/in/test"},
                "location_identifiers": [{"value": "New York"}],
                "category_groups": [{"value": "FinTech"}, {"value": "AI"}],
            }
        }

        result = prospecting_service._parse_crunchbase_entity(entity)

        assert result is not None
        assert result["name"] == "Test VC"
        assert result["investor_type"] == "vc"
        assert result["linkedin_url"] == "https://linkedin.com/in/test"
        assert result["location"] == "New York"
        assert "FinTech" in result["focus_areas"]
        assert "AI" in result["focus_areas"]
        assert result["source"] == "crunchbase"
        assert "raw_data" in result

    def test_parse_crunchbase_entity_invalid(
        self, prospecting_service: ProspectingService
    ):
        """Test parsing an invalid Crunchbase entity returns None."""
        entity = {"properties": {}}  # Missing name
        result = prospecting_service._parse_crunchbase_entity(entity)
        assert result is None

    def test_extract_focus_areas(self, prospecting_service: ProspectingService):
        """Test extracting focus areas from category groups."""
        properties = {
            "category_groups": [
                {"value": "AI"},
                {"value": "Machine Learning"},
                {"value": "Robotics"},
            ]
        }

        focus_areas = prospecting_service._extract_focus_areas(properties)

        assert focus_areas == ["AI", "Machine Learning", "Robotics"]

    def test_extract_focus_areas_empty(self, prospecting_service: ProspectingService):
        """Test extracting focus areas with empty category groups."""
        properties = {"category_groups": []}
        focus_areas = prospecting_service._extract_focus_areas(properties)
        assert focus_areas == []

    async def test_fetch_angellist_investors_no_token(
        self, prospecting_service: ProspectingService
    ):
        """Test that AngelList fetch returns empty when no access token."""
        from pitcherai.config import get_get_settings()

        original_token = get_settings().angellist_access_token
        get_settings().angellist_access_token = None

        result = await prospecting_service.fetch_angellist_investors(
            query="AI", limit=10
        )

        assert result == []
        get_settings().angellist_access_token = original_token

    async def test_fetch_angellist_investors_success(
        self, prospecting_service: ProspectingService
    ):
        """Test successful AngelList fetch with mocked response."""
        from pitcherai.config import get_get_settings()

        if not get_settings().angellist_access_token:
            pytest.skip("AngelList access token not configured")

        prospecting_service.client = AsyncMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "investors": [
                {
                    "name": "Angel Investor",
                    "type": "angel",
                    "company": {"name": "AngelGroup"},
                    "email": "angel@example.com",
                    "linkedin_url": "https://linkedin.com/in/angel",
                    "tags": ["Startups", "Tech"],
                    "location": {"name": "San Francisco"},
                }
            ]
        }
        mock_response.raise_for_status = MagicMock()
        prospecting_service.client.get.return_value = mock_response

        result = await prospecting_service.fetch_angellist_investors(
            query="AI", limit=10
        )

        assert len(result) == 1
        assert result[0]["name"] == "Angel Investor"
        assert result[0]["investor_type"] == "angel"
        assert result[0]["source"] == "angellist"

    def test_parse_angellist_investor_valid(
        self, prospecting_service: ProspectingService
    ):
        """Test parsing a valid AngelList investor."""
        investor_data = {
            "name": "John Angel",
            "type": "vc",
            "company": {"name": "VC Fund"},
            "email": "john@vc.com",
            "linkedin_url": "https://linkedin.com/in/john",
            "tags": ["AI", "Deep Tech"],
            "location": {"name": "Boston"},
        }

        result = prospecting_service._parse_angellist_investor(investor_data)

        assert result is not None
        assert result["name"] == "John Angel"
        assert result["investor_type"] == "vc"
        assert result["firm_name"] == "VC Fund"
        assert result["email"] == "john@vc.com"
        assert result["focus_areas"] == ["AI", "Deep Tech"]
        assert result["location"] == "Boston"
        assert result["source"] == "angellist"

    def test_parse_angellist_investor_invalid(
        self, prospecting_service: ProspectingService
    ):
        """Test parsing invalid AngelList data returns None."""
        investor_data = {}  # Missing name
        result = prospecting_service._parse_angellist_investor(investor_data)
        assert result is None

    async def test_import_investors_from_sources(
        self, session: AsyncSession, prospecting_service: ProspectingService
    ):
        """Test importing investors from sources."""
        # Mock the fetch methods
        prospecting_service.fetch_crunchbase_investors = AsyncMock(
            return_value=[
                {
                    "name": "Crunchbase Investor",
                    "investor_type": "vc",
                    "firm_name": "CB Ventures",
                    "email": "cb@test.com",
                    "focus_areas": ["AI"],
                    "location": "SF",
                    "source": "crunchbase",
                }
            ]
        )
        prospecting_service.fetch_angellist_investors = AsyncMock(
            return_value=[
                {
                    "name": "AngelList Investor",
                    "investor_type": "angel",
                    "firm_name": "AngelGroup",
                    "email": "al@test.com",
                    "focus_areas": ["SaaS"],
                    "location": "NY",
                    "source": "angellist",
                }
            ]
        )

        # Mock crud.investor.get_by_email to return None (no existing investor)
        original_get_by_email = crud.investor.get_by_email

        async def mock_get_by_email(session, email):
            return None

        crud.investor.get_by_email = mock_get_by_email

        total = await prospecting_service.import_investors_from_sources(
            session,
            queries=["AI"],
            sources=["crunchbase", "angellist"],
            limit_per_source=10,
        )

        assert total == 2

        # Verify investors were created
        investors = await crud.investor.get_multi(session, limit=10)
        assert len(investors) >= 2
        names = [inv.name for inv in investors]
        assert "Crunchbase Investor" in names
        assert "AngelList Investor" in names

        # Restore original
        crud.investor.get_by_email = original_get_by_email

    async def test_import_investors_from_sources_skips_duplicates(
        self,
        session: AsyncSession,
        prospecting_service: ProspectingService,
        db_investor: Investor,
    ):
        """Test that importing skips existing investors."""
        prospecting_service.fetch_crunchbase_investors = AsyncMock(
            return_value=[
                {
                    "name": "Duplicate Investor",
                    "investor_type": "vc",
                    "email": db_investor.email,  # Use existing investor's email
                    "focus_areas": ["AI"],
                    "source": "crunchbase",
                }
            ]
        )

        # Mock get_by_email to return the existing investor
        original_get_by_email = crud.investor.get_by_email

        async def mock_get_by_email(session, email):
            if email == db_investor.email:
                return db_investor
            return None

        crud.investor.get_by_email = mock_get_by_email

        total = await prospecting_service.import_investors_from_sources(
            session, queries=["AI"], sources=["crunchbase"], limit_per_source=10
        )

        assert total == 0  # Should not import duplicate

        crud.investor.get_by_email = original_get_by_email

    async def test_import_investors_from_sources_unknown_source(
        self, session: AsyncSession, prospecting_service: ProspectingService
    ):
        """Test that unknown sources are skipped."""
        total = await prospecting_service.import_investors_from_sources(
            session, queries=["AI"], sources=["unknown_source"], limit_per_source=10
        )
        assert total == 0

    async def test_enrich_investor_portfolio_no_crunchbase_id(
        self,
        session: AsyncSession,
        prospecting_service: ProspectingService,
        db_investor: Investor,
    ):
        """Test portfolio enrichment when investor has no Crunchbase ID."""
        # Ensure investor has no crunchbase_id in raw_data
        db_investor.raw_data = {}
        await session.commit()

        added = await prospecting_service.enrich_investor_portfolio(
            session, db_investor.id
        )
        assert added == 0

    async def test_enrich_investor_portfolio_with_crunchbase(
        self,
        session: AsyncSession,
        prospecting_service: ProspectingService,
        db_investor: Investor,
    ):
        """Test portfolio enrichment from Crunchbase."""
        from pitcherai.config import get_get_settings()

        if not get_settings().crunchbase_api_key:
            pytest.skip("Crunchbase API key not configured")

        # Add crunchbase_id to investor
        db_investor.raw_data = {"crunchbase_id": "org123"}
        await session.commit()

        # Mock the httpx client
        prospecting_service.client = AsyncMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "entities": {
                "inv1": {
                    "properties": {
                        "company_name": "StartupX",
                        "funding_type": "Seed",
                        "announced_date": "2024-01-15",
                    }
                }
            }
        }
        mock_response.raise_for_status = MagicMock()
        prospecting_service.client.get.return_value = mock_response

        added = await prospecting_service.enrich_investor_portfolio(
            session, db_investor.id
        )

        # Should have added at least one investment
        assert added >= 1

    async def test_enrich_investor_portfolio_nonexistent_investor(
        self, session: AsyncSession, prospecting_service: ProspectingService
    ):
        """Test enrichment for non-existent investor."""
        from uuid import uuid4

        fake_id = uuid4()
        added = await prospecting_service.enrich_investor_portfolio(session, fake_id)
        assert added == 0

    async def test_close_client(self, prospecting_service: ProspectingService):
        """Test closing the HTTP client."""
        prospecting_service.client = AsyncMock()
        await prospecting_service.close()
        prospecting_service.client.aclose.assert_called_once()
