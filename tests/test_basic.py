"""Basic tests for PitcherAI core functionality"""

import pytest
from datetime import datetime
from src.database.models import (
    Investor,
    EmailTemplate,
    Email,
    Campaign,
    InvestorStatus,
    EmailStatus,
)
from src.config.config import Settings


def test_settings_defaults():
    """Test that settings loads with defaults"""
    settings = Settings()
    assert settings.database_url == "sqlite:///pitcherai.db"
    assert settings.openai_model == "gpt-4-turbo-preview"
    assert settings.max_emails_per_day == 50
    assert settings.default_draft_template is not None


def test_investor_creation():
    """Test Investor model creation"""
    investor = Investor(
        name="John Doe",
        email="john@example.com",
        firm="Test Ventures",
        title="General Partner",
        relevance_score=0.85,
    )
    assert investor.name == "John Doe"
    assert investor.email == "john@example.com"
    assert investor.relevance_score == 0.85
    assert investor.status == InvestorStatus.PROSPECT


def test_email_template_creation():
    """Test EmailTemplate model creation"""
    template = EmailTemplate(
        name="Test Template",
        subject="Investment Opportunity",
        body="Hi {{name}}, I'm reaching out about {{company}}.",
    )
    assert template.name == "Test Template"
    assert template.subject == "Investment Opportunity"
    assert template.status.value == "active"


def test_investor_scoring_simple():
    """Simple test of investor scoring logic"""
    from src.targeter import InvestorScorer

    user_profile = {
        "focus_areas": ["AI/ML", "Enterprise SaaS"],
        "preferred_stages": ["Seed", "Series A"],
    }

    scorer = InvestorScorer(user_profile)

    investor = Investor(
        name="Test Investor",
        firm="AI Fund",
        focus_areas='["AI/ML"]',
        investment_stage="Seed",
        last_funding_date=datetime.utcnow(),
    )

    score = scorer.calculate_relevance(investor)
    assert 0 <= score <= 1.0
    # Should score higher due to matching focus area and stage
    assert score > 0.3


def test_database_integrity():
    """Test that all models have required fields"""
    # Test that models can be instantiated with minimal data
    investor = Investor(name="Test")
    assert investor.name == "Test"

    template = EmailTemplate(name="T", subject="S", body="B")
    assert template.name == "T"

    campaign = Campaign(name="Campaign")
    assert campaign.name == "Campaign"
