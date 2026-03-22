"""Pytest configuration and shared fixtures."""

import asyncio
from datetime import datetime, timezone, date
from typing import AsyncGenerator, Generator
from uuid import UUID, uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from pitcherai.database import Base
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
)
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


# SQLite in-memory database for testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def engine():
    """Create a test database engine."""
    from sqlalchemy.ext.asyncio import create_async_engine

    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        poolclass=StaticPool,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    await engine.dispose()


@pytest.fixture
async def session(engine) -> AsyncGenerator[AsyncSession, None]:
    """Create a fresh database session for each test."""
    from sqlalchemy.ext.asyncio import async_sessionmaker

    TestSessionLocal = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with TestSessionLocal() as session:
        yield session
        await session.rollback()


@pytest.fixture
def sample_uuid() -> UUID:
    """Return a fixed UUID for testing."""
    return UUID("12345678-1234-5678-1234-567812345678")


@pytest.fixture
def sample_user(sample_uuid: UUID) -> dict:
    """Sample user data."""
    return {
        "id": sample_uuid,
        "email": "test@example.com",
        "startup_name": "TestStartup",
        "startup_description": "A test startup",
        "niche": "tech",
    }


@pytest.fixture
async def db_user(session: AsyncSession, sample_user: dict) -> User:
    """Create a user in the database."""
    user = User(
        id=sample_user["id"],
        email=sample_user["email"],
        startup_name=sample_user["startup_name"],
        startup_description=sample_user["startup_description"],
        niche=sample_user["niche"],
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@pytest.fixture
def sample_investor(sample_uuid: UUID) -> dict:
    """Sample investor data."""
    return {
        "id": sample_uuid,
        "name": "John Doe",
        "investor_type": "vc",
        "firm_name": "Test Ventures",
        "email": "john@testventures.com",
        "linkedin_url": "https://linkedin.com/in/johndoe",
        "focus_areas": ["AI", "Machine Learning"],
        "stage_preferences": ["Seed", "Series A"],
        "location": "San Francisco",
        "source": "crunchbase",
    }


@pytest.fixture
async def db_investor(session: AsyncSession, sample_investor: dict) -> Investor:
    """Create an investor in the database."""
    investor = Investor(**sample_investor)
    session.add(investor)
    await session.commit()
    await session.refresh(investor)
    return investor


@pytest.fixture
def sample_investment(sample_uuid: UUID, sample_investor: dict) -> dict:
    """Sample investment data."""
    return {
        "id": uuid4(),
        "investor_id": sample_investor["id"],
        "startup_name": "AnotherStartup",
        "investment_date": date(2024, 1, 15),
        "round_type": "Seed",
        "amount_usd": 1000000.0,
        "source": "crunchbase",
    }


@pytest.fixture
async def db_investment(session: AsyncSession, sample_investment: dict) -> Investment:
    """Create an investment in the database."""
    investment = Investment(**sample_investment)
    session.add(investment)
    await session.commit()
    await session.refresh(investment)
    return investment


@pytest.fixture
def sample_template(sample_uuid: UUID) -> dict:
    """Sample template data."""
    return {
        "id": sample_uuid,
        "name": "Initial Outreach",
        "subject_template": "Introduction: {{user_startup}}",
        "body_template": "Hello {{investor_name}}, I'm building {{user_startup}}...",
        "variant_id": "v1",
        "is_active": True,
    }


@pytest.fixture
async def db_template(session: AsyncSession, sample_template: dict) -> Template:
    """Create a template in the database."""
    template = Template(**sample_template)
    session.add(template)
    await session.commit()
    await session.refresh(template)
    return template


@pytest.fixture
def sample_campaign(
    sample_uuid: UUID, sample_user: dict, sample_template: dict
) -> dict:
    """Sample campaign data."""
    return {
        "id": sample_uuid,
        "user_id": sample_user["id"],
        "name": "Seed Round Outreach",
        "status": "draft",
        "template_id": sample_template["id"],
        "target_criteria": {"focus_areas": ["AI"], "investor_types": ["vc"]},
    }


@pytest.fixture
async def db_campaign(session: AsyncSession, sample_campaign: dict) -> Campaign:
    """Create a campaign in the database."""
    campaign = Campaign(**sample_campaign)
    session.add(campaign)
    await session.commit()
    await session.refresh(campaign)
    return campaign


@pytest.fixture
def sample_campaign_target(
    sample_uuid: UUID, sample_campaign: dict, sample_investor: dict
) -> dict:
    """Sample campaign target data."""
    return {
        "id": sample_uuid,
        "campaign_id": sample_campaign["id"],
        "investor_id": sample_investor["id"],
        "status": "pending",
        "email_subject": None,
        "email_body": None,
        "scheduled_send_at": None,
        "sent_at": None,
        "user_override_notes": None,
    }


@pytest.fixture
async def db_campaign_target(
    session: AsyncSession, sample_campaign_target: dict
) -> CampaignTarget:
    """Create a campaign target in the database."""
    target = CampaignTarget(**sample_campaign_target)
    session.add(target)
    await session.commit()
    await session.refresh(target)
    return target
