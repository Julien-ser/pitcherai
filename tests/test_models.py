"""Tests for data models."""

import pytest
from datetime import datetime
from src.models import Investor, Startup, EmailTemplate, Outreach, Campaign


def test_investor_creation():
    """Test investor model creation."""
    investor = Investor(
        id="inv_001",
        name="John Doe",
        email="john@example.com",
        firm="ABC Ventures",
        focus_areas=["AI", "SaaS"],
        stage_preference=["seed", "series-a"],
    )
    assert investor.id == "inv_001"
    assert "AI" in investor.focus_areas
    assert investor.firm == "ABC Ventures"


def test_startup_creation():
    """Test startup model creation."""
    startup = Startup(
        id="startup_001",
        name="My Startup",
        industry="AI",
        stage="seed",
        description="An AI startup",
        funding_needed=2000000,
    )
    assert startup.name == "My Startup"
    assert startup.stage == "seed"
    assert startup.funding_needed == 2_000_000


def test_email_template_creation():
    """Test email template model."""
    template = EmailTemplate(
        id="tpl_001",
        name="Cold Intro",
        subject="Investment Opportunity: {startup_name}",
        body="Dear {investor_name}, We're building...",
        variant="cold_pitch",
    )
    assert template.variant == "cold_pitch"
    assert "{startup_name}" in template.subject


def test_outreach_status_flow():
    """Test outreach status transitions."""
    outreach = Outreach(
        id="out_001",
        campaign_id="camp_001",
        investor_id="inv_001",
        subject="Test Email",
        body="Test content",
    )
    assert outreach.status == "draft"
    outreach.status = "queued"
    assert outreach.status == "queued"
    outreach.status = "sent"
    assert outreach.status == "sent"
