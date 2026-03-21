"""Tests for target filtering."""

import pytest
from src.models import Investor, Startup
from src.targeter import TargetFilter


@pytest.fixture
def sample_startup():
    return Startup(
        id="startup_001",
        name="AI Startup",
        industry="AI",
        stage="seed",
        description="AI company",
        funding_needed=1500000,
    )


@pytest.fixture
def sample_investors():
    return [
        Investor(
            id="inv_001",
            name="Alice AI",
            email="alice@vc.com",
            firm="AI Ventures",
            focus_areas=["AI", "ML"],
            stage_preference=["seed", "series-a"],
            portfolio=["AI Co 1"],
        ),
        Investor(
            id="inv_002",
            name="Bob SaaS",
            email="bob@vc.com",
            firm="SaaS Fund",
            focus_areas=["SaaS", "B2B"],
            stage_preference=["series-a", "series-b"],
            portfolio=["SaaS Co 1"],
        ),
    ]


def test_filter_by_stage(sample_startup, sample_investors):
    """Test stage filtering."""
    filt = TargetFilter(sample_startup)
    filtered = filt.filter_by_stage(sample_investors)
    assert len(filtered) == 1
    assert filtered[0].id == "inv_001"  # seed stage investor


def test_filter_by_industry(sample_startup, sample_investors):
    """Test industry filtering."""
    filt = TargetFilter(sample_startup)
    filtered = filt.filter_by_industry(sample_investors)
    assert len(filtered) == 1
    assert filtered[0].id == "inv_001"  # AI focused investor


def test_combined_filters(sample_startup, sample_investors):
    """Test combined filters."""
    filt = TargetFilter(sample_startup)
    filtered = filt.filter(sample_investors)
    assert len(filtered) == 1
    assert filtered[0].id == "inv_001"
