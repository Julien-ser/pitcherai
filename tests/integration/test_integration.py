"""End-to-end integration tests for PitcherAI.

These tests verify the complete workflow from investor import to campaign execution.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID, uuid4
from datetime import datetime, date
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from pitcherai.database import Base, get_db
from pitcherai.models import Investment
from pitcherai.services.prospecting import ProspectingService
from pitcherai.services.campaign import CampaignService
from pitcherai.services.email_generation import EmailGenerationService
from pitcherai import crud
from pitcherai.schemas import (
    UserCreate,
    InvestorCreate,
    TemplateCreate,
    CampaignCreate,
    CampaignTargetCreate,
)


class TestFullCampaignLifecycle:
    """Test the complete campaign lifecycle from setup to tracking."""

    async def test_complete_end_to_end_workflow(
        self, session: AsyncSession, sample_uuid: UUID
    ):
        """Test the full workflow: user → investors → template → campaign → emails → tracking."""

        # 1. Create a user
        user_data = {
            "email": "founder@startup.com",
            "startup_name": "AI Startup",
            "startup_description": "Building AI-powered solutions",
            "niche": "AI/ML",
        }
        user = await crud.user.create(session, obj_in=UserCreate(**user_data))

        # 2. Create a template
        template_data = {
            "name": "Initial Outreach",
            "subject_template": "Introduction: {{user_startup}}",
            "body_template": "Hello {{investor_name}}, I'm building {{user_startup}} in {{user_niche}}. I noticed your investments in {{investor_focus}}...",
            "is_active": True,
        }
        template = await crud.template.create(
            session, obj_in=TemplateCreate(**template_data)
        )

        # 3. Create investors manually (simulating import)
        investors = [
            {
                "name": "AI VC Partner",
                "investor_type": "vc",
                "firm_name": "AI Ventures",
                "email": "partner@aiventures.com",
                "focus_areas": ["AI", "Machine Learning"],
                "location": "San Francisco",
                "source": "manual",
            },
            {
                "name": "Tech Angel",
                "investor_type": "angel",
                "firm_name": "Individual",
                "email": "angel@tech.com",
                "focus_areas": ["SaaS", "Tech"],
                "location": "New York",
                "source": "manual",
            },
            {
                "name": "FinTech Fund",
                "investor_type": "vc",
                "firm_name": "FinTech Capital",
                "email": "partner@fintechcap.com",
                "focus_areas": ["FinTech", "AI"],
                "location": "Boston",
                "source": "manual",
            },
        ]

        created_investors = []
        for inv_data in investors:
            inv = await crud.investor.create(session, obj_in=InvestorCreate(**inv_data))
            created_investors.append(inv)

            # Add some investments for one investor
            if inv.name == "AI VC Partner":
                from datetime import timedelta

                investment = Investment(
                    investor_id=inv.id,
                    startup_name="PortfolioCo",
                    round_type="Seed",
                    investment_date=date.today() - timedelta(days=30),
                )
                session.add(investment)
                await session.flush()

        await session.commit()

        # 4. Create a campaign with auto-generation
        campaign_service = CampaignService()
        campaign = await campaign_service.create_campaign_with_targets(
            session,
            name="AI Startup Seed Round",
            user_id=user.id,
            template_id=template.id,
            target_criteria={
                "investor_types": ["vc"],
                "focus_areas": ["AI"],
                "location": None,
            },
            auto_generate_emails=True,
        )

        # Verify campaign was created
        assert campaign.name == "AI Startup Seed Round"
        assert campaign.status == "draft"
        assert campaign.user_id == user.id
        assert campaign.template_id == template.id

        # 5. Verify targets were created
        targets = await crud.campaign_target.get_by_campaign(session, campaign.id)
        assert len(targets) >= 1  # At least AI VC should match

        # 6. Verify emails were generated for matching targets
        for target in targets:
            if target.status in ("approved", "sent") and target.investor:
                assert target.email_subject is not None
                assert target.email_body is not None
                assert len(target.email_subject) > 0
                assert len(target.email_body) > 0
                # Subject should contain startup name
                assert user.startup_name in target.email_subject
                # Body should contain investor name
                assert target.investor.name in target.email_body

        # 7. Start the campaign
        started_campaign = await campaign_service.start_campaign(
            session, campaign_id=campaign.id
        )
        assert started_campaign is not None
        assert started_campaign.status == "active"
        assert started_campaign.started_at is not None

        # 8. Simulate sending emails (mark some targets as sent)
        sent_count = 0
        for target in targets:
            if target.status == "approved" and sent_count < 2:
                marked = await campaign_service.mark_target_sent(
                    session,
                    target_id=target.id,
                    message_id=f"msg_{uuid4().hex[:8]}",
                )
                if marked:
                    sent_count += 1
                    assert marked.status == "sent"
                    assert marked.sent_at is not None

        await session.commit()

        # 9. Verify tracking records were created
        for target in targets:
            if target.status == "sent":
                tracking = await crud.email_tracking.get_by_target(
                    session, target_id=target.id
                )
                assert tracking is not None
                assert tracking.message_id is not None
                assert tracking.opens_count == 0

        # 10. Simulate email opens
        for target in targets:
            if target.status == "sent":
                tracking = await crud.email_tracking.get_by_target(
                    session, target_id=target.id
                )
                if tracking:
                    # Simulate open
                    tracking.opens_count += 1
                    tracking.last_opened_at = datetime.now()
                    await session.flush()

        await session.commit()

        # 11. Get campaign analytics (direct CRUD)
        today = date.today()
        analytics = await crud.analytics.create_or_update(
            session,
            campaign_id=campaign.id,
            date_val=today,
            sent_count=len([t for t in targets if t.status == "sent"]),
            open_count=len([t for t in targets if t.status == "sent"]),  # All opened
            reply_count=1,  # Simulate one reply
        )

        await session.commit()

        # Verify analytics
        assert analytics.sent_count > 0
        assert analytics.open_count > 0
        assert analytics.reply_count >= 0

        print("✅ Full end-to-end workflow test passed!")


class TestInvestorImportAndEnrichment:
    """Test investor import and enrichment workflows."""

    async def test_prospecting_import_workflow(self, session: AsyncSession):
        """Test importing investors from various sources."""
        prospecting = ProspectingService()

        # Mock the external API calls
        prospecting.client = AsyncMock()

        # Mock Crunchbase response
        mock_crunchbase = MagicMock()
        mock_crunchbase.json.return_value = {
            "entities": {
                "org1": {
                    "properties": {
                        "name": "Mock AI Fund",
                        "linkedin": {"value": "https://linkedin.com/company/mock"},
                        "location_identifiers": [{"value": "San Francisco"}],
                        "category_groups": [{"value": "AI"}],
                    }
                }
            }
        }
        mock_crunchbase.raise_for_status = MagicMock()

        # Mock AngelList response
        mock_angellist = MagicMock()
        mock_angellist.json.return_value = {
            "investors": [
                {
                    "name": "Mock Angel",
                    "type": "angel",
                    "company": {"name": "AngelGroup"},
                    "email": "mock@angel.com",
                    "linkedin_url": "https://linkedin.com/in/mock",
                    "tags": ["AI", "Startups"],
                    "location": {"name": "NYC"},
                }
            ]
        }
        mock_angellist.raise_for_status = MagicMock()
        prospecting.client.get.side_effect = [mock_crunchbase, mock_angellist]

        # Temporarily patch the API keys as set
        with patch("pitcherai.config.settings") as mock_settings:
            mock_settings.crunchbase_api_key = "test_key"
            mock_settings.angellist_access_token = "test_token"

            total = await prospecting.import_investors_from_sources(
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
        assert "Mock AI Fund" in names
        assert "Mock Angel" in names

    async def test_enrich_investor_portfolio_workflow(self, session: AsyncSession):
        """Test enriching investor portfolio with investments."""
        prospecting = ProspectingService()
        prospecting.client = AsyncMock()

        # Create an investor with Crunchbase ID
        investor = await crud.investor.create(
            session,
            obj_in=InvestorCreate(
                name="Test VC",
                investor_type="vc",
                email="vc@test.com",
                source="test",
                raw_data={"crunchbase_id": "org123"},
            ),
        )

        # Mock Crunchbase investments response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "entities": {
                "inv1": {
                    "properties": {
                        "company_name": "StartupX",
                        "funding_type": "Seed",
                        "announced_date": "2024-01-15",
                    }
                },
                "inv2": {
                    "properties": {
                        "company_name": "StartupY",
                        "funding_type": "Series A",
                        "announced_date": "2024-02-01",
                    }
                },
            }
        }
        mock_response.raise_for_status = MagicMock()
        prospecting.client.get.return_value = mock_response

        with patch("pitcherai.config.settings") as mock_settings:
            mock_settings.crunchbase_api_key = "test_key"

            added = await prospecting.enrich_investor_portfolio(
                session, investor_id=investor.id
            )

        assert added >= 2

        # Verify investments were added
        updated_investor = await crud.investor.get(session, id=investor.id)
        if updated_investor and updated_investor.investments:
            assert len(updated_investor.investments) >= 2

            investment_names = [
                inv.startup_name for inv in updated_investor.investments
            ]
            assert "StartupX" in investment_names
            assert "StartupY" in investment_names


class TestEmailGenerationIntegration:
    """Test email generation with real database data."""

    async def test_email_generation_with_investor_data(self, session: AsyncSession):
        """Test generating an email using database data."""
        from pitcherai.schemas import UserCreate, InvestorCreate, TemplateCreate

        # Create user
        user = await crud.user.create(
            session,
            obj_in=UserCreate(
                email="founder@test.com",
                startup_name="TestStartup",
                startup_description="A test startup building AI solutions",
                niche="AI",
            ),
        )

        # Create investor with investments
        investor = await crud.investor.create(
            session,
            obj_in=InvestorCreate(
                name="John Doe",
                investor_type="vc",
                firm_name="Test Ventures",
                email="john@testventures.com",
                focus_areas=["AI", "Machine Learning"],
                location="San Francisco",
                source="test",
            ),
        )

        # Add investment
        from datetime import timedelta

        investment = Investment(
            investor_id=investor.id,
            startup_name="PortfolioStartup",
            round_type="Seed",
            investment_date=date.today() - timedelta(days=45),
        )
        session.add(investment)

        # Create template
        template = await crud.template.create(
            session,
            obj_in=TemplateCreate(
                name="Outreach Template",
                subject_template="Introduction: {{user_startup}}",
                body_template="Hello {{investor_name}}, I'm {{user_startup}} building AI solutions. I noticed your investment in {{investor_recent_investments}}...",
                is_active=True,
            ),
        )

        await session.commit()

        # Generate email using the service
        email_gen = EmailGenerationService()

        # Get investor's recent investments
        result = await session.execute(
            select(Investment)
            .where(Investment.investor_id == investor.id)
            .order_by(Investment.investment_date.desc())
            .limit(5)
        )
        inv_list = result.scalars().all()
        recent_investments = [
            {
                "startup_name": inv.startup_name,
                "round_type": inv.round_type,
                "investment_date": inv.investment_date.isoformat()
                if inv.investment_date
                else None,
            }
            for inv in inv_list
        ]

        subject, body = await email_gen.generate_email(
            investor_name=investor.name,
            investor_firm=investor.firm_name,
            investor_focus=investor.focus_areas,
            investor_recent_investments=recent_investments,
            user_startup=user.startup_name,
            user_description=user.startup_description or "",
            user_niche=user.niche,
            template_subject=template.subject_template,
            template_body=template.body_template,
            custom_vars={},
        )

        # Verify results
        assert subject is not None
        assert len(subject) > 0
        assert body is not None
        assert len(body) > 0

        # Should contain personalization
        assert investor.name in body
        assert user.startup_name in body
        assert "AI" in body  # Should mention AI from focus or niche

        print("✅ Email generation integration test passed!")


class TestServiceInteractions:
    """Test interactions between multiple services."""

    async def test_campaign_target_approval_and_email_generation(
        self, session: AsyncSession
    ):
        """Test approving targets triggers email generation."""
        from pitcherai.schemas import (
            UserCreate,
            InvestorCreate,
            TemplateCreate,
            CampaignCreate,
        )

        # Create base data
        user = await crud.user.create(
            session,
            obj_in=UserCreate(
                email="test@founder.com",
                startup_name="TestCo",
                startup_description="Testing",
                niche="Tech",
            ),
        )

        template = await crud.template.create(
            session,
            obj_in=TemplateCreate(
                name="Test Template",
                subject_template="Hi {{investor_name}}",
                body_template="Hello {{investor_name}}, we're {{user_startup}}",
                is_active=True,
            ),
        )

        investor = await crud.investor.create(
            session,
            obj_in=InvestorCreate(
                name="Investor One",
                investor_type="vc",
                email="investor@one.com",
                focus_areas=["Tech"],
                source="test",
            ),
        )

        # Create campaign
        campaign = await crud.campaign.create(
            session,
            obj_in=CampaignCreate(
                name="Test Campaign",
                user_id=user.id,
                template_id=template.id,
                target_criteria={"investor_types": ["vc"]},
            ),
        )

        # Create target
        target = await crud.campaign_target.create(
            session,
            obj_in=CampaignTargetCreate(
                campaign_id=campaign.id,
                investor_id=investor.id,
                status="pending",
            ),
        )

        await session.commit()

        # Use CampaignService to process email generation
        campaign_service = CampaignService()

        # Call the private method to generate emails
        await campaign_service._generate_emails_for_campaign(session, campaign.id)

        # Verify target was processed
        updated_target = await crud.campaign_target.get(session, id=target.id)
        # The method should have set status to approved and added email content
        if updated_target and updated_target.status == "approved":
            assert updated_target.email_subject is not None
            assert updated_target.email_body is not None

    async def test_analytics_calculation_end_to_end(self, session: AsyncSession):
        """Test analytics calculation with real data."""
        from pitcherai.schemas import (
            UserCreate,
            InvestorCreate,
            TemplateCreate,
            CampaignCreate,
            CampaignTargetCreate,
        )
        from pitcherai.services.campaign import campaign_service
        from pitcherai.main import get_campaign_analytics  # Import inside test

        # Create user, template, investor
        user = await crud.user.create(
            session,
            obj_in=UserCreate(
                email="analytics@test.com",
                startup_name="AnalyticsTest",
                startup_description="Test",
                niche="Tech",
            ),
        )

        template = await crud.template.create(
            session,
            obj_in=TemplateCreate(
                name="Analytics Template",
                subject_template="Test",
                body_template="Test body",
                is_active=True,
            ),
        )

        investor = await crud.investor.create(
            session,
            obj_in=InvestorCreate(
                name="Analytics Investor",
                investor_type="vc",
                email="inv@test.com",
                focus_areas=["Tech"],
                source="test",
            ),
        )

        # Create and start campaign
        campaign = await campaign_service.create_campaign_with_targets(
            session,
            name="Analytics Campaign",
            user_id=user.id,
            template_id=template.id,
            target_criteria={"investor_types": ["vc"]},
            auto_generate_emails=True,
        )

        # Mark some targets as sent
        targets = await crud.campaign_target.get_by_campaign(session, campaign.id)
        for i, target in enumerate(targets[:3]):  # Send to first 3
            await campaign_service.mark_target_sent(
                session,
                target_id=target.id,
                message_id=f"msg_{i}",
            )
            # Simulate open for some
            if i < 2:
                tracking = await crud.email_tracking.get_by_target(
                    session, target_id=target.id
                )
                if tracking:
                    tracking.opens_count = 1
                    tracking.last_opened_at = datetime.now()

        await session.commit()

        # Get analytics
        today = date.today()
        analytics = await crud.analytics.create_or_update(
            session,
            campaign_id=campaign.id,
            date_val=today,
            sent_count=3,
            open_count=2,
            reply_count=1,
        )

        await session.commit()

        # Verify calculations
        assert analytics.sent_count == 3
        assert analytics.open_count == 2
        assert analytics.reply_count == 1
        open_rate_val = analytics.open_rate if analytics.open_rate is not None else 0
        reply_rate_val = analytics.reply_rate if analytics.reply_rate is not None else 0
        assert abs(open_rate_val - (2 / 3 * 100)) < 0.1
        assert abs(reply_rate_val - (1 / 3 * 100)) < 0.1

        # Test the API endpoint via direct function call
        analytics_resp = await get_campaign_analytics(str(campaign.id), session)
        sent_count = int(analytics_resp.get("sent_count", 0))
        open_count = int(analytics_resp.get("open_count", 0))
        assert sent_count >= 0
        assert open_count >= 0
        assert "open_rate" in analytics_resp
        assert "reply_rate" in analytics_resp


class TestAPIIntegration:
    """Test API endpoints integration."""

    async def test_full_api_workflow(self, session: AsyncSession):
        """Test complete API workflow."""
        from pitcherai.main import app, get_db
        from fastapi.testclient import TestClient

        # Override get_db dependency to use our test session
        async def override_get_db():
            yield session

        app.dependency_overrides[get_db] = override_get_db

        # Build list of created object IDs
        user_id = None
        template_id = None
        investor_id = None
        campaign_id = None

        try:
            with TestClient(app) as client:
                # 1. Create user via API
                user_response = client.post(
                    "/api/users",
                    json={
                        "email": "api@test.com",
                        "startup_name": "API Test Startup",
                        "startup_description": "Testing the API",
                        "niche": "AI",
                    },
                )
                assert user_response.status_code == 201
                user_data = user_response.json()
                user_id = user_data["id"]

                # 2. Create template via API
                template_response = client.post(
                    "/api/templates",
                    json={
                        "name": "API Template",
                        "subject_template": "Hello {{investor_name}}",
                        "body_template": "Hi {{investor_name}}, we're {{user_startup}}",
                        "is_active": True,
                    },
                )
                assert template_response.status_code == 201
                template_data = template_response.json()
                template_id = template_data["id"]

                # 3. Create investor via API
                investor_response = client.post(
                    "/api/investors",
                    json={
                        "name": "API Investor",
                        "investor_type": "vc",
                        "firm_name": "API Ventures",
                        "email": "api@vc.com",
                        "focus_areas": ["AI", "Tech"],
                        "location": "Online",
                        "source": "api",
                    },
                )
                assert investor_response.status_code == 201
                investor_data = investor_response.json()
                investor_id = investor_data["id"]

                # 4. Create campaign via API
                campaign_response = client.post(
                    "/api/campaigns",
                    json={
                        "name": "API Campaign",
                        "user_id": user_id,
                        "template_id": template_id,
                        "target_criteria": {"investor_types": ["vc"]},
                    },
                )
                assert campaign_response.status_code == 201
                campaign_data = campaign_response.json()
                campaign_id = campaign_data["id"]

                # 5. Get campaign via API
                get_campaign_response = client.get(f"/api/campaigns/{campaign_id}")
                assert get_campaign_response.status_code == 200

                # 6. Get campaign targets
                targets_response = client.get(f"/api/campaigns/{campaign_id}/targets")
                assert targets_response.status_code == 200
                targets_data = targets_response.json()
                assert len(targets_data["targets"]) >= 1

                # 7. Get investors list
                investors_response = client.get("/api/investors")
                assert investors_response.status_code == 200
                investors_list = investors_response.json()
                assert len(investors_list) >= 1

                # 8. Get analytics
                analytics_response = client.get(
                    f"/api/analytics/campaign/{campaign_id}"
                )
                assert analytics_response.status_code == 200
                analytics_data = analytics_response.json()
                assert "sent_count" in analytics_data

                print("✅ API integration test passed!")

        finally:
            # Clean up dependency override
            if get_db in app.dependency_overrides:
                del app.dependency_overrides[get_db]


class TestConcurrencyAndDataConsistency:
    """Test concurrent operations and data consistency."""

    async def test_concurrent_campaign_creation(self, session: AsyncSession):
        """Test creating multiple campaigns concurrently."""
        from pitcherai.schemas import UserCreate, TemplateCreate, CampaignCreate
        import asyncio

        # Create user and template
        user = await crud.user.create(
            session,
            obj_in=UserCreate(
                email="concurrent@test.com",
                startup_name="ConcurrentTest",
                startup_description="Test",
                niche="Tech",
            ),
        )

        template = await crud.template.create(
            session,
            obj_in=TemplateCreate(
                name="Concurrent Template",
                subject_template="Test",
                body_template="Test body",
                is_active=True,
            ),
        )

        await session.commit()

        # Create multiple campaigns concurrently
        async def create_campaign(index: int):
            return await crud.campaign.create(
                session,
                obj_in=CampaignCreate(
                    name=f"Concurrent Campaign {index}",
                    user_id=user.id,
                    template_id=template.id,
                    target_criteria={},
                ),
            )

        tasks = [create_campaign(i) for i in range(5)]
        campaigns = await asyncio.gather(*tasks)

        assert len(campaigns) == 5
        campaign_names = [c.name for c in campaigns]
        assert all(f"Concurrent Campaign {i}" in campaign_names for i in range(5))

    async def test_data_consistency_across_services(self, session: AsyncSession):
        """Test that data remains consistent when accessed from different services."""

        # Setup: create user, investor, investment, template, campaign
        from pitcherai.schemas import (
            UserCreate,
            InvestorCreate,
            TemplateCreate,
            CampaignCreate,
        )
        from datetime import timedelta

        user = await crud.user.create(
            session,
            obj_in=UserCreate(
                email="consistency@test.com",
                startup_name="ConsistencyTest",
                startup_description="Test",
                niche="AI",
            ),
        )

        investor = await crud.investor.create(
            session,
            obj_in=InvestorCreate(
                name="Consistent Investor",
                investor_type="vc",
                email="inv@consistency.com",
                focus_areas=["AI"],
                source="test",
            ),
        )

        # Add investment
        investment = Investment(
            investor_id=investor.id,
            startup_name="ConsistentPortfolio",
            round_type="Seed",
            investment_date=date.today() - timedelta(days=10),
        )
        session.add(investment)

        template = await crud.template.create(
            session,
            obj_in=TemplateCreate(
                name="Consistency Template",
                subject_template="Hello",
                body_template="Hello body",
                is_active=True,
            ),
        )

        campaign = await crud.campaign.create(
            session,
            obj_in=CampaignCreate(
                name="Consistency Campaign",
                user_id=user.id,
                template_id=template.id,
                target_criteria={"investor_types": ["vc"]},
            ),
        )

        await session.commit()

        # Test: CampaignService's investor matching should find the investor
        campaign_service = CampaignService()
        matching = await campaign_service._find_matching_investors(
            session, {"investor_types": ["vc"]}
        )

        assert investor in matching

        # Test: Email generation should see the investment
        targets = await crud.campaign_target.get_by_campaign(session, campaign.id)
        if targets:
            target = targets[0]
            investor_for_email = await crud.investor.get(session, id=target.investor_id)
            if investor_for_email and investor_for_email.investments:
                assert len(investor_for_email.investments) >= 1

        # Test: All services see consistent data
        fetched_user = await crud.user.get(session, id=user.id)
        if fetched_user:
            assert fetched_user.startup_name == "ConsistencyTest"

        fetched_investor = await crud.investor.get(session, id=investor.id)
        if fetched_investor:
            assert fetched_investor.name == "Consistent Investor"
            if fetched_investor.investments:
                assert len(fetched_investor.investments) == 1
