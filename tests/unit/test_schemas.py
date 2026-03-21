"""Tests for Pydantic schemas."""

import pytest
from uuid import UUID, uuid4
from datetime import datetime, timezone
from pydantic import ValidationError

from pitcherai.schemas import (
    UserCreate,
    UserUpdate,
    UserResponse,
    InvestorCreate,
    InvestorUpdate,
    InvestorResponse,
    TemplateCreate,
    TemplateUpdate,
    TemplateResponse,
    CampaignCreate,
    CampaignUpdate,
    CampaignResponse,
    CampaignTargetCreate,
    CampaignTargetUpdate,
    CampaignTargetResponse,
    EmailGenerateRequest,
    EmailGenerateResponse,
)


def test_user_create_valid():
    """Test valid user creation."""
    user_data = {
        "email": "test@example.com",
        "startup_name": "TestStartup",
        "startup_description": "A test startup",
        "niche": "tech",
    }
    user = UserCreate(**user_data)
    assert user.email == "test@example.com"
    assert user.startup_name == "TestStartup"
    assert user.niche == "tech"


def test_user_create_invalid_email():
    """Test that invalid email raises validation error."""
    with pytest.raises(ValidationError):
        UserCreate(email="invalid-email", startup_name="Test", niche="tech")


def test_user_update_partial():
    """Test partial user update."""
    update_data = {"startup_name": "UpdatedName", "niche": "fintech"}
    user_update = UserUpdate(**update_data)
    assert user_update.startup_name == "UpdatedName"
    assert user_update.niche == "fintech"
    assert user_update.email is None


def test_investor_create_valid():
    """Test valid investor creation."""
    investor_data = {
        "name": "John Doe",
        "investor_type": "vc",
        "firm_name": "Test Ventures",
        "email": "john@test.com",
        "focus_areas": ["AI", "ML"],
        "stage_preferences": ["Seed", "Series A"],
        "location": "San Francisco",
        "source": "crunchbase",
    }
    investor = InvestorCreate(**investor_data)
    assert investor.name == "John Doe"
    assert investor.investor_type == "vc"
    assert investor.focus_areas == ["AI", "ML"]


def test_investor_create_invalid_type():
    """Test that invalid investor type raises validation error."""
    with pytest.raises(ValidationError):
        InvestorCreate(name="John", investor_type="invalid", source="test")


def test_template_create_valid():
    """Test valid template creation."""
    template_data = {
        "name": "Initial Outreach",
        "subject_template": "Hello {{investor_name}}",
        "body_template": "Hi {{investor_name}}, we're {{user_startup}}",
        "variant_id": "v1",
        "is_active": True,
    }
    template = TemplateCreate(**template_data)
    assert template.name == "Initial Outreach"
    assert template.subject_template == "Hello {{investor_name}}"
    assert template.is_active is True


def test_campaign_create_valid():
    """Test valid campaign creation."""
    campaign_data = {
        "name": "Seed Round Campaign",
        "user_id": uuid4(),
        "template_id": uuid4(),
        "target_criteria": {"focus": ["AI"]},
    }
    campaign = CampaignCreate(**campaign_data)
    assert campaign.name == "Seed Round Campaign"
    # status has default value 'draft' in CampaignBase
    assert campaign.status == "draft"


def test_campaign_target_create_valid():
    """Test valid campaign target creation."""
    target_data = {
        "campaign_id": uuid4(),
        "investor_id": uuid4(),
        "status": "pending",
    }
    target = CampaignTargetCreate(**target_data)
    assert target.status == "pending"


def test_email_generate_request_valid():
    """Test valid email generation request."""
    request_data = {
        "investor_id": uuid4(),
        "template_id": uuid4(),
        "user_id": uuid4(),
        "custom_vars": {"custom_key": "custom_value"},
    }
    request = EmailGenerateRequest(**request_data)
    assert request.custom_vars == {"custom_key": "custom_value"}


def test_email_generate_response_valid():
    """Test email generation response."""
    response = EmailGenerateResponse(subject="Test Subject", body="Test Body")
    assert response.subject == "Test Subject"
    assert response.body == "Test Body"
