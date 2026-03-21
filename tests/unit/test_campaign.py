"""Tests for Campaign service."""

import pytest
from uuid import UUID, uuid4
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, date
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from pitcherai.services.campaign import CampaignService
from pitcherai.models import Investor
from pitcherai import crud
from pitcherai.schemas import (
    UserCreate,
    TemplateCreate,
    CampaignCreate,
    CampaignTargetCreate,
    CampaignTargetUpdate,
    InvestorCreate,
)


class TestCampaignService:
    """Tests for CampaignService."""

    async def test_create_campaign_with_targets_no_auto_generate(
        self, session: AsyncSession, sample_user: dict, sample_template: dict
    ):
        """Test creating a campaign without auto-generating emails."""
        service = CampaignService()

        # Create user and template first
        user = await crud.user.create(session, obj_in=UserCreate(**sample_user))
        template = await crud.template.create(
            session, obj_in=TemplateCreate(**sample_template)
        )

        campaign = await service.create_campaign_with_targets(
            session,
            name="Test Campaign",
            user_id=user.id,
            template_id=template.id,
            target_criteria={"investor_types": ["vc"]},
            auto_generate_emails=False,
        )

        assert campaign.name == "Test Campaign"
        assert campaign.status == "draft"

        # Verify no targets were created (no investors in DB yet)
        targets = await crud.campaign_target.get_by_campaign(session, campaign.id)
        assert len(targets) == 0

    async def test_create_campaign_with_targets_with_auto_generate(
        self,
        session: AsyncSession,
        sample_user: dict,
        sample_template: dict,
        db_investor: Investor,
    ):
        """Test creating a campaign with auto-generating emails (but no targets if criteria mismatch)."""
        service = CampaignService()

        user = await crud.user.create(session, obj_in=UserCreate(**sample_user))
        template = await crud.template.create(
            session, obj_in=TemplateCreate(**sample_template)
        )

        # Create campaign with criteria that matches the db_investor
        # db_investor has focus_areas=["AI", "Machine Learning"] from fixture
        campaign = await service.create_campaign_with_targets(
            session,
            name="AI Outreach Campaign",
            user_id=user.id,
            template_id=template.id,
            target_criteria={
                "investor_types": ["vc"],
                "focus_areas": ["AI"],
            },
            auto_generate_emails=True,
        )

        assert campaign.name == "AI Outreach Campaign"

        # Should have created a target for the matching investor
        targets = await crud.campaign_target.get_by_campaign(session, campaign.id)
        assert len(targets) >= 1  # At least the AI-focused investor should match

    async def test_find_matching_investors(
        self, session: AsyncSession, sample_user: dict, sample_template: dict
    ):
        """Test the investor matching logic."""
        service = CampaignService()

        # Create some investors with different attributes
        inv1 = InvestorCreate(
            name="AI VC",
            investor_type="vc",
            email="ai_vc@test.com",
            focus_areas=["AI", "ML"],
            location="San Francisco",
            source="test",
        )
        inv2 = InvestorCreate(
            name="FinTech Angel",
            investor_type="angel",
            email="fintech_angel@test.com",
            focus_areas=["FinTech"],
            location="New York",
            source="test",
        )
        inv3 = InvestorCreate(
            name="SaaS VC",
            investor_type="vc",
            email="saas_vc@test.com",
            focus_areas=["SaaS"],
            location="San Francisco",
            source="test",
        )

        from pitcherai.schemas import InvestorCreate

        await crud.investor.create(session, obj_in=inv1)
        await crud.investor.create(session, obj_in=inv2)
        await crud.investor.create(session, obj_in=inv3)

        # Test filter by investor type
        vcs = await service._find_matching_investors(
            session, {"investor_types": ["vc"]}
        )
        assert len(vcs) >= 2  # Should include AI VC and SaaS VC
        assert all(v.investor_type == "vc" for v in vcs)

        # Test filter by focus area
        ai_investors = await service._find_matching_investors(
            session, {"focus_areas": ["AI"]}
        )
        assert len(ai_investors) >= 1
        assert any("AI" in (inv.focus_areas or []) for inv in ai_investors)

        # Test filter by location
        sf_investors = await service._find_matching_investors(
            session, {"location": "San Francisco"}
        )
        assert len(sf_investors) >= 2
        # Note: location might be None for some investors, check if it contains San Francisco when not None
        assert all(
            inv.location and "San Francisco" in inv.location for inv in sf_investors
        )

        # Test combined filters
        sf_vcs = await service._find_matching_investors(
            session, {"investor_types": ["vc"], "location": "San Francisco"}
        )
        assert len(sf_vcs) >= 2
        assert all(
            v.investor_type == "vc" and (v.location and "San Francisco" in v.location)
            for v in sf_vcs
        )

    async def test_get_pending_targets(
        self, session: AsyncSession, sample_campaign: dict, sample_investor: dict
    ):
        """Test getting pending (approved or not sent) targets."""
        service = CampaignService()

        # Create campaign
        campaign = await crud.campaign.create(
            session, obj_in=CampaignCreate(**sample_campaign)
        )

        # Create targets with different statuses
        target1 = CampaignTargetCreate(
            campaign_id=campaign.id,
            investor_id=sample_investor["id"],
            status="pending",
        )
        target2 = CampaignTargetCreate(
            campaign_id=campaign.id,
            investor_id=sample_investor["id"],
            status="approved",
        )
        target3 = CampaignTargetCreate(
            campaign_id=campaign.id,
            investor_id=sample_investor["id"],
            status="sent",
        )

        await crud.campaign_target.create(session, obj_in=target1)
        await crud.campaign_target.create(session, obj_in=target2)
        await crud.campaign_target.create(session, obj_in=target3)

        pending = await service.get_pending_targets(session, campaign.id)
        assert len(pending) == 2  # pending and approved, but not sent
        statuses = [t.status for t in pending]
        assert "pending" in statuses
        assert "approved" in statuses
        assert "sent" not in statuses

    async def test_approve_target(
        self, session: AsyncSession, sample_campaign_target: dict
    ):
        """Test approving a campaign target."""
        service = CampaignService()

        target = await crud.campaign_target.create(
            session, obj_in=CampaignTargetCreate(**sample_campaign_target)
        )

        approved = await service.approve_target(session, target_id=target.id)
        assert approved is not None
        assert approved.status == "approved"
        assert approved.user_override_notes is None

    async def test_approve_target_with_override(
        self, session: AsyncSession, sample_campaign_target: dict
    ):
        """Test approving with override notes."""
        service = CampaignService()

        target = await crud.campaign_target.create(
            session, obj_in=CampaignTargetCreate(**sample_campaign_target)
        )

        approved = await service.approve_target(
            session, target_id=target.id, override_notes="Custom message"
        )
        assert approved is not None
        assert approved.status == "approved"
        assert approved.user_override_notes == "Custom message"

    async def test_reject_target(
        self, session: AsyncSession, sample_campaign_target: dict
    ):
        """Test rejecting a campaign target."""
        service = CampaignService()

        target = await crud.campaign_target.create(
            session, obj_in=CampaignTargetCreate(**sample_campaign_target)
        )

        rejected = await service.reject_target(
            session, target_id=target.id, reason="Not a fit"
        )
        assert rejected is not None
        assert rejected.status == "rejected"
        assert rejected.user_override_notes == "Not a fit"

    async def test_start_campaign(self, session: AsyncSession, sample_campaign: dict):
        """Test starting a campaign."""
        service = CampaignService()

        campaign = await crud.campaign.create(
            session, obj_in=CampaignCreate(**sample_campaign)
        )
        assert campaign.status == "draft"

        started = await service.start_campaign(session, campaign_id=campaign.id)
        assert started is not None
        assert started.status == "active"
        assert started.started_at is not None

    async def test_mark_target_sent(
        self, session: AsyncSession, sample_campaign_target: dict
    ):
        """Test marking a target as sent and creating tracking."""
        service = CampaignService()

        target = await crud.campaign_target.create(
            session, obj_in=CampaignTargetCreate(**sample_campaign_target)
        )

        marked = await service.mark_target_sent(
            session, target_id=target.id, message_id="msg_12345"
        )
        assert marked is not None
        assert marked.status == "sent"
        assert marked.sent_at is not None

        # Verify tracking record was created
        tracking = await crud.email_tracking.get_by_target(session, target_id=target.id)
        assert tracking is not None
        assert tracking.message_id == "msg_12345"
        assert tracking.opens_count == 0

    async def test_generate_emails_for_campaign_integration(
        self,
        session: AsyncSession,
        sample_user: dict,
        sample_template: dict,
        db_investor: Investor,
    ):
        """Test email generation for campaign targets (integration test)."""
        service = CampaignService()

        user = await crud.user.create(session, obj_in=UserCreate(**sample_user))
        template = await crud.template.create(
            session, obj_in=TemplateCreate(**sample_template)
        )

        # Create campaign with auto-generate
        campaign = await service.create_campaign_with_targets(
            session,
            name="Test Email Gen Campaign",
            user_id=user.id,
            template_id=template.id,
            target_criteria={
                "investor_types": ["vc"],
                "focus_areas": ["AI"],
            },
            auto_generate_emails=True,
        )

        # Check that emails were generated
        targets = await crud.campaign_target.get_by_campaign(session, campaign.id)
        assert len(targets) >= 1

        for target in targets:
            # Email should be generated
            if target.status in ("approved", "sent"):
                assert target.email_subject is not None
                assert target.email_body is not None
                assert len(target.email_subject) > 0
                assert len(target.email_body) > 0
