"""Tests for SQLAlchemy models."""

import pytest
from datetime import datetime, timezone, date
from uuid import UUID, uuid4

from pitcherai.models import (
    User,
    Investor,
    Investment,
    SharedConnection,
    Template,
    Campaign,
    CampaignTarget,
    EmailTracking,
    Analytics,
    TimestampMixin,
)


def test_user_model(sample_uuid):
    """Test User model creation and attributes."""
    user = User(
        id=sample_uuid,
        email="test@example.com",
        startup_name="TestStartup",
        startup_description="A test startup",
        niche="tech",
    )
    assert user.email == "test@example.com"
    assert user.startup_name == "TestStartup"
    assert user.niche == "tech"
    assert user.id == sample_uuid


def test_investor_model(sample_uuid):
    """Test Investor model creation and attributes."""
    investor = Investor(
        id=sample_uuid,
        name="John Doe",
        investor_type="vc",
        firm_name="Test Ventures",
        email="john@test.com",
        focus_areas=["AI", "ML"],
        stage_preferences=["Seed"],
        location="San Francisco",
        source="crunchbase",
    )
    assert investor.name == "John Doe"
    assert investor.investor_type == "vc"
    assert investor.focus_areas == ["AI", "ML"]
    assert investor.source == "crunchbase"


def test_investment_model(sample_uuid):
    """Test Investment model creation."""
    investment = Investment(
        id=uuid4(),
        investor_id=sample_uuid,
        startup_name="TestStartup",
        investment_date=date(2024, 1, 15),
        round_type="Seed",
        amount_usd=1000000.0,
        source="crunchbase",
    )
    assert investment.startup_name == "TestStartup"
    assert investment.amount_usd == 1000000.0
    assert investment.round_type == "Seed"


def test_shared_connection_model(sample_uuid):
    """Test SharedConnection model creation."""
    connection = SharedConnection(
        id=uuid4(),
        user_id=sample_uuid,
        investor_id=sample_uuid,
        connection_name="Jane Smith",
        connection_email="jane@example.com",
        relationship_type="colleague",
    )
    assert connection.connection_name == "Jane Smith"
    assert connection.relationship_type == "colleague"


def test_template_model(sample_uuid):
    """Test Template model creation."""
    template = Template(
        id=sample_uuid,
        name="Initial Outreach",
        subject_template="Hello {{investor_name}}",
        body_template="Hi {{investor_name}}, we're {{user_startup}}",
        variant_id="v1",
        is_active=True,
    )
    assert template.name == "Initial Outreach"
    assert template.is_active is True
    assert "{{investor_name}}" in template.subject_template


def test_campaign_model(sample_uuid):
    """Test Campaign model creation."""
    campaign = Campaign(
        id=sample_uuid,
        user_id=sample_uuid,
        name="Seed Round Campaign",
        status="draft",
    )
    assert campaign.name == "Seed Round Campaign"
    assert campaign.status == "draft"


def test_campaign_target_model(sample_uuid):
    """Test CampaignTarget model creation."""
    target = CampaignTarget(
        id=uuid4(),
        campaign_id=sample_uuid,
        investor_id=sample_uuid,
        status="pending",
    )
    assert target.status == "pending"


def test_email_tracking_model(sample_uuid):
    """Test EmailTracking model creation."""
    tracking = EmailTracking(
        id=uuid4(),
        campaign_target_id=sample_uuid,
        message_id="msg_123",
        opens_count=0,
        clicks_count=0,
    )
    assert tracking.message_id == "msg_123"
    assert tracking.opens_count == 0


def test_analytics_model(sample_uuid):
    """Test Analytics model creation."""
    analytics = Analytics(
        id=uuid4(),
        campaign_id=sample_uuid,
        date=date(2024, 1, 15),
        sent_count=100,
        open_count=25,
        click_count=5,
        reply_count=3,
    )
    assert analytics.sent_count == 100
    assert analytics.open_count == 25
    assert analytics.open_rate == 25.0  # 25/100 * 100
    assert analytics.reply_rate == 3.0  # 3/100 * 100
