"""Tests for CRUD operations."""

import pytest
from uuid import UUID, uuid4
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession

from pitcherai.crud import (
    user,
    investor,
    template,
    campaign,
    campaign_target,
    email_tracking,
    analytics,
)
from pitcherai.models import User, Investor, Template, Campaign, CampaignTarget
from pitcherai.schemas import (
    UserCreate,
    UserUpdate,
    InvestorCreate,
    InvestorUpdate,
    TemplateCreate,
    TemplateUpdate,
    CampaignCreate,
    CampaignUpdate,
    CampaignTargetCreate,
    CampaignTargetUpdate,
)


class TestUserCRUD:
    """Tests for UserCRUD operations."""

    async def test_create_user(self, session: AsyncSession, sample_user: dict):
        """Test creating a new user."""
        user_data = UserCreate(**sample_user)
        db_user = await user.create(session, obj_in=user_data)
        assert db_user.id == sample_user["id"]
        assert db_user.email == sample_user["email"]
        assert db_user.startup_name == sample_user["startup_name"]

    async def test_get_user(self, session: AsyncSession, db_user: User):
        """Test retrieving a user by ID."""
        retrieved = await user.get(session, id=db_user.id)
        assert retrieved is not None
        assert retrieved.id == db_user.id
        assert retrieved.email == db_user.email

    async def test_get_by_email(self, session: AsyncSession, db_user: User):
        """Test retrieving a user by email."""
        retrieved = await user.get_by_email(session, email=db_user.email)
        assert retrieved is not None
        assert retrieved.id == db_user.id

    async def test_update_user(self, session: AsyncSession, db_user: User):
        """Test updating a user."""
        update_data = UserUpdate(startup_name="Updated Startup", niche="fintech")
        updated = await user.update(session, db_obj=db_user, obj_in=update_data)
        assert updated.startup_name == "Updated Startup"
        assert updated.niche == "fintech"
        assert updated.email == db_user.email  # unchanged

    async def test_delete_user(self, session: AsyncSession, db_user: User):
        """Test deleting a user."""
        result = await user.delete(session, id=db_user.id)
        assert result is True
        # Verify deletion
        deleted = await user.get(session, id=db_user.id)
        assert deleted is None

    async def test_get_multi(self, session: AsyncSession, db_user: User):
        """Test retrieving multiple users with pagination."""
        # Create another user
        user2_data = UserCreate(
            email="test2@example.com",
            startup_name="TestStartup2",
            startup_description="Another test",
            niche="ai",
        )
        await user.create(session, obj_in=user2_data)

        users = await user.get_multi(session, skip=0, limit=10)
        assert len(users) >= 2
        assert any(u.email == db_user.email for u in users)


class TestInvestorCRUD:
    """Tests for InvestorCRUD operations."""

    async def test_create_investor(self, session: AsyncSession, sample_investor: dict):
        """Test creating a new investor."""
        investor_data = InvestorCreate(**sample_investor)
        db_investor = await investor.create(session, obj_in=investor_data)
        assert db_investor.id == sample_investor["id"]
        assert db_investor.name == sample_investor["name"]
        assert db_investor.investor_type == sample_investor["investor_type"]

    async def test_get_investor(self, session: AsyncSession, db_investor: Investor):
        """Test retrieving an investor by ID."""
        retrieved = await investor.get(session, id=db_investor.id)
        assert retrieved is not None
        assert retrieved.id == db_investor.id
        assert retrieved.name == db_investor.name

    async def test_update_investor(self, session: AsyncSession, db_investor: Investor):
        """Test updating an investor."""
        update_data = InvestorUpdate(
            firm_name="Updated Ventures", focus_areas=["AI", "Deep Learning"]
        )
        updated = await investor.update(session, db_obj=db_investor, obj_in=update_data)
        assert updated.firm_name == "Updated Ventures"
        assert updated.focus_areas == ["AI", "Deep Learning"]

    async def test_delete_investor(self, session: AsyncSession, db_investor: Investor):
        """Test deleting an investor."""
        result = await investor.delete(session, id=db_investor.id)
        assert result is True
        deleted = await investor.get(session, id=db_investor.id)
        assert deleted is None

    async def test_search_by_focus(self, session: AsyncSession, sample_investor: dict):
        """Test searching investors by focus area."""
        # Create multiple investors with different focus areas
        inv1 = InvestorCreate(
            name="Investor 1",
            investor_type="vc",
            email="inv1@test.com",
            focus_areas=["AI", "ML"],
            source="test",
        )
        inv2 = InvestorCreate(
            name="Investor 2",
            investor_type="angel",
            email="inv2@test.com",
            focus_areas=["SaaS", "B2B"],
            source="test",
        )
        inv3 = InvestorCreate(
            name="Investor 3",
            investor_type="vc",
            email="inv3@test.com",
            focus_areas=["AI", "FinTech"],
            source="test",
        )

        await investor.create(session, obj_in=inv1)
        await investor.create(session, obj_in=inv2)
        await investor.create(session, obj_in=inv3)

        ai_investors = await investor.search_by_focus(session, focus_area="AI")
        assert len(ai_investors) >= 2
        assert all("AI" in (inv.focus_areas or []) for inv in ai_investors)

    async def test_list_by_type(self, session: AsyncSession, sample_investor: dict):
        """Test listing investors by type."""
        vc_data = InvestorCreate(
            name="VC Investor",
            investor_type="vc",
            email="vc@test.com",
            focus_areas=["Tech"],
            source="test",
        )
        angel_data = InvestorCreate(
            name="Angel Investor",
            investor_type="angel",
            email="angel@test.com",
            focus_areas=["Tech"],
            source="test",
        )
        await investor.create(session, obj_in=vc_data)
        await investor.create(session, obj_in=angel_data)

        vcs = await investor.list_by_type(session, investor_type="vc")
        assert len(vcs) >= 1
        assert all(v.investor_type == "vc" for v in vcs)


class TestTemplateCRUD:
    """Tests for TemplateCRUD operations."""

    async def test_create_template(self, session: AsyncSession, sample_template: dict):
        """Test creating a template."""
        template_data = TemplateCreate(**sample_template)
        db_template = await template.create(session, obj_in=template_data)
        assert db_template.id == sample_template["id"]
        assert db_template.name == sample_template["name"]
        assert db_template.is_active is True

    async def test_get_template(self, session: AsyncSession, db_template: Template):
        """Test retrieving a template."""
        retrieved = await template.get(session, id=db_template.id)
        assert retrieved is not None
        assert retrieved.name == db_template.name

    async def test_update_template(self, session: AsyncSession, db_template: Template):
        """Test updating a template."""
        update_data = TemplateUpdate(
            name="Updated Template", body_template="New body content"
        )
        updated = await template.update(session, db_obj=db_template, obj_in=update_data)
        assert updated.name == "Updated Template"
        assert updated.body_template == "New body content"

    async def test_delete_template(self, session: AsyncSession, db_template: Template):
        """Test deleting a template."""
        result = await template.delete(session, id=db_template.id)
        assert result is True
        deleted = await template.get(session, id=db_template.id)
        assert deleted is None

    async def test_get_active(self, session: AsyncSession):
        """Test getting only active templates."""
        active_data = TemplateCreate(
            name="Active Template",
            subject_template="Hello",
            body_template="Hi there",
            is_active=True,
        )
        inactive_data = TemplateCreate(
            name="Inactive Template",
            subject_template="Hello",
            body_template="Hi there",
            is_active=False,
        )
        await template.create(session, obj_in=active_data)
        await template.create(session, obj_in=inactive_data)

        active_templates = await template.get_active(session)
        assert len(active_templates) >= 1
        assert all(t.is_active for t in active_templates)


class TestCampaignCRUD:
    """Tests for CampaignCRUD operations."""

    async def test_create_campaign(
        self, session: AsyncSession, sample_campaign: dict, sample_user: dict
    ):
        """Test creating a campaign."""
        campaign_data = CampaignCreate(**sample_campaign)
        db_campaign = await campaign.create(session, obj_in=campaign_data)
        assert db_campaign.id == sample_campaign["id"]
        assert db_campaign.name == sample_campaign["name"]
        assert db_campaign.status == "draft"

    async def test_get_campaign(self, session: AsyncSession, db_campaign: Campaign):
        """Test retrieving a campaign."""
        retrieved = await campaign.get(session, id=db_campaign.id)
        assert retrieved is not None
        assert retrieved.name == db_campaign.name

    async def test_update_campaign(self, session: AsyncSession, db_campaign: Campaign):
        """Test updating a campaign."""
        update_data = CampaignUpdate(
            name="Updated Campaign", target_criteria={"focus_areas": ["FinTech"]}
        )
        updated = await campaign.update(session, db_obj=db_campaign, obj_in=update_data)
        assert updated.name == "Updated Campaign"
        assert updated.target_criteria == {"focus_areas": ["FinTech"]}

    async def test_start_campaign(self, session: AsyncSession, db_campaign: Campaign):
        """Test starting a campaign."""
        started = await campaign.start_campaign(session, campaign_id=db_campaign.id)
        assert started is not None
        assert started.status == "active"
        assert started.started_at is not None

    async def test_get_by_user(
        self, session: AsyncSession, sample_campaign: dict, sample_user: dict
    ):
        """Test getting campaigns by user."""
        # Create the sample user in the database
        db_user = await user.create(session, obj_in=UserCreate(**sample_user))

        # Create a campaign for the sample user
        campaign_data = CampaignCreate(**sample_campaign)
        await campaign.create(session, obj_in=campaign_data)

        # Create another campaign for a different user
        other_user_data = UserCreate(
            email="other@example.com",
            startup_name="Other Startup",
            niche="health",
        )
        other_user = await user.create(session, obj_in=other_user_data)

        campaign2_data = CampaignCreate(
            name="User 2 Campaign",
            user_id=other_user.id,
            template_id=sample_campaign["template_id"],
            target_criteria={},
        )
        await campaign.create(session, obj_in=campaign2_data)

        user_campaigns = await campaign.get_by_user(session, user_id=sample_user["id"])
        assert all(c.user_id == sample_user["id"] for c in user_campaigns)
        assert any(c.name == sample_campaign["name"] for c in user_campaigns)


class TestCampaignTargetCRUD:
    """Tests for CampaignTargetCRUD operations."""

    async def test_create_campaign_target(
        self, session: AsyncSession, db_campaign: Campaign, db_investor: Investor
    ):
        """Test creating a campaign target."""
        target_data = CampaignTargetCreate(
            campaign_id=db_campaign.id, investor_id=db_investor.id, status="pending"
        )
        db_target = await campaign_target.create(session, obj_in=target_data)
        assert db_target.campaign_id == db_campaign.id
        assert db_target.investor_id == db_investor.id
        assert db_target.status == "pending"

    async def test_get_by_campaign(
        self, session: AsyncSession, db_campaign: Campaign, db_investor: Investor
    ):
        """Test getting targets by campaign."""
        target_data = CampaignTargetCreate(
            campaign_id=db_campaign.id, investor_id=db_investor.id, status="pending"
        )
        await campaign_target.create(session, obj_in=target_data)

        targets = await campaign_target.get_by_campaign(
            session, campaign_id=db_campaign.id
        )
        assert len(targets) >= 1
        assert all(t.campaign_id == db_campaign.id for t in targets)

    async def test_get_pending(
        self, session: AsyncSession, db_campaign: Campaign, db_investor: Investor
    ):
        """Test getting pending targets."""
        # Create targets with different statuses
        pending_data = CampaignTargetCreate(
            campaign_id=db_campaign.id, investor_id=db_investor.id, status="pending"
        )
        approved_data = CampaignTargetCreate(
            campaign_id=db_campaign.id, investor_id=db_investor.id, status="approved"
        )
        await campaign_target.create(session, obj_in=pending_data)
        await campaign_target.create(session, obj_in=approved_data)

        pending = await campaign_target.get_pending(session, campaign_id=db_campaign.id)
        assert len(pending) >= 1
        assert all(t.status in ("pending", "approved") for t in pending)

    async def test_mark_sent(
        self, session: AsyncSession, db_campaign: Campaign, db_investor: Investor
    ):
        """Test marking a target as sent."""
        target_data = CampaignTargetCreate(
            campaign_id=db_campaign.id, investor_id=db_investor.id, status="approved"
        )
        target = await campaign_target.create(session, obj_in=target_data)

        marked = await campaign_target.mark_sent(session, target_id=target.id)
        assert marked is not None
        assert marked.status == "sent"
        assert marked.sent_at is not None


class TestEmailTrackingCRUD:
    """Tests for EmailTrackingCRUD operations."""

    async def test_create_tracking(
        self, session: AsyncSession, db_campaign_target: CampaignTarget
    ):
        """Test creating an email tracking record."""
        tracking = await email_tracking.create(
            session, target_id=db_campaign_target.id, message_id="msg_123"
        )
        assert tracking.campaign_target_id == db_campaign_target.id
        assert tracking.message_id == "msg_123"
        assert tracking.opens_count == 0

    async def test_update_open(
        self, session: AsyncSession, db_campaign_target: CampaignTarget
    ):
        """Test incrementing open count."""
        tracking = await email_tracking.create(session, target_id=db_campaign_target.id)
        updated = await email_tracking.update_open(
            session, target_id=db_campaign_target.id
        )
        assert updated is not None
        assert updated.opens_count == 1
        assert updated.last_opened_at is not None

    async def test_update_reply(
        self, session: AsyncSession, db_campaign_target: CampaignTarget
    ):
        """Test marking as replied."""
        tracking = await email_tracking.create(session, target_id=db_campaign_target.id)
        updated = await email_tracking.update_reply(
            session, target_id=db_campaign_target.id
        )
        assert updated is not None
        assert updated.replied_at is not None


class TestAnalyticsCRUD:
    """Tests for AnalyticsCRUD operations."""

    async def test_create_or_update_existing(
        self, session: AsyncSession, db_campaign: Campaign
    ):
        """Test creating new analytics record."""
        today = date.today()
        analytics_obj = await analytics.create_or_update(
            session,
            campaign_id=db_campaign.id,
            date_val=today,
            sent_count=50,
            open_count=10,
            click_count=5,
            reply_count=2,
        )
        assert analytics_obj.campaign_id == db_campaign.id
        assert analytics_obj.sent_count == 50
        assert analytics_obj.open_count == 10
        assert analytics_obj.open_rate == 20.0  # 10/50 * 100
        assert analytics_obj.reply_rate == 4.0  # 2/50 * 100

    async def test_create_or_update_update_existing(
        self, session: AsyncSession, db_campaign: Campaign
    ):
        """Test updating existing analytics record."""
        today = date.today()

        # Create initial record
        await analytics.create_or_update(
            session,
            campaign_id=db_campaign.id,
            date_val=today,
            sent_count=50,
            open_count=10,
            click_count=5,
            reply_count=2,
        )

        # Update with new values
        updated = await analytics.create_or_update(
            session,
            campaign_id=db_campaign.id,
            date_val=today,
            sent_count=100,
            open_count=30,
            click_count=10,
            reply_count=5,
        )
        assert updated.sent_count == 100
        assert updated.open_count == 30
        assert updated.open_rate == 30.0

    async def test_get_by_campaign_date(
        self, session: AsyncSession, db_campaign: Campaign
    ):
        """Test retrieving analytics by campaign and date."""
        today = date.today()
        await analytics.create_or_update(
            session,
            campaign_id=db_campaign.id,
            date_val=today,
            sent_count=50,
            open_count=10,
        )

        retrieved = await analytics.get_by_campaign_date(
            session, campaign_id=db_campaign.id, date_val=today
        )
        assert retrieved is not None
        assert retrieved.sent_count == 50
