"""Database module."""

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from typing import Generator

from src.config import settings
from src.models_db import (
    init_db,
    get_sessionmaker,
    InvestorDB,
    StartupDB,
    CampaignDB,
    EmailTemplateDB,
    OutreachDB,
    FundingAnnouncementDB,
)

_engine = None
_SessionLocal = None


def get_engine():
    """Get or create database engine."""
    global _engine, _SessionLocal
    if _engine is None:
        _engine = create_engine(
            settings.database_url,
            echo=settings.debug,
            pool_pre_ping=True,
        )
        _SessionLocal = get_sessionmaker(_engine)
        init_db(_engine)
    return _engine


def get_session() -> Generator[Session, None, None]:
    """Get database session."""
    global _SessionLocal
    if _SessionLocal is None:
        get_engine()
    session = _SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


# Database repositories for CRUD operations
class InvestorRepository:
    """Investor database repository."""

    def __init__(self, session: Session):
        self.session = session

    def create(self, investor_data: dict) -> InvestorDB:
        """Create new investor."""
        investor = InvestorDB(**investor_data)
        self.session.add(investor)
        self.session.flush()
        return investor

    def get_by_id(self, investor_id: str) -> InvestorDB:
        """Get investor by ID."""
        return self.session.query(InvestorDB).get(investor_id)

    def get_by_email(self, email: str) -> InvestorDB:
        """Get investor by email."""
        return self.session.query(InvestorDB).filter_by(email=email).first()

    def list_all(self, limit: int = 100, offset: int = 0) -> list[InvestorDB]:
        """List all investors."""
        return self.session.query(InvestorDB).limit(limit).offset(offset).all()

    def update(self, investor_id: str, **kwargs) -> InvestorDB:
        """Update investor."""
        investor = self.get_by_id(investor_id)
        for key, value in kwargs.items():
            setattr(investor, key, value)
        return investor

    def upsert(self, investor_data: dict) -> InvestorDB:
        """Create or update investor."""
        email = investor_data.get("email")
        if email:
            existing = self.get_by_email(email)
            if existing:
                for key, value in investor_data.items():
                    if key != "id" and hasattr(existing, key):
                        setattr(existing, key, value)
                return existing
        return self.create(investor_data)


class StartupRepository:
    """Startup database repository."""

    def __init__(self, session: Session):
        self.session = session

    def create(self, startup_data: dict) -> StartupDB:
        """Create new startup."""
        startup = StartupDB(**startup_data)
        self.session.add(startup)
        self.session.flush()
        return startup

    def get_by_id(self, startup_id: str) -> StartupDB:
        """Get startup by ID."""
        return self.session.query(StartupDB).get(startup_id)

    def get_by_name(self, name: str) -> StartupDB:
        """Get startup by name."""
        return self.session.query(StartupDB).filter_by(name=name).first()


class CampaignRepository:
    """Campaign database repository."""

    def __init__(self, session: Session):
        self.session = session

    def create(self, campaign_data: dict) -> CampaignDB:
        """Create new campaign."""
        campaign = CampaignDB(**campaign_data)
        self.session.add(campaign)
        self.session.flush()
        return campaign

    def get_by_id(self, campaign_id: str) -> CampaignDB:
        """Get campaign by ID."""
        return self.session.query(CampaignDB).get(campaign_id)

    def list_by_startup(self, startup_id: str) -> list[CampaignDB]:
        """List campaigns for a startup."""
        return (
            self.session.query(CampaignDB)
            .filter_by(startup_id=startup_id)
            .order_by(CampaignDB.created_at.desc())
            .all()
        )


class OutreachRepository:
    """Outreach database repository."""

    def __init__(self, session: Session):
        self.session = session

    def create(self, outreach_data: dict) -> OutreachDB:
        """Create new outreach."""
        outreach = OutreachDB(**outreach_data)
        self.session.add(outreach)
        self.session.flush()
        return outreach

    def get_by_id(self, outreach_id: str) -> OutreachDB:
        """Get outreach by ID."""
        return self.session.query(OutreachDB).get(outreach_id)

    def get_by_campaign(self, campaign_id: str) -> list[OutreachDB]:
        """Get all outreaches for a campaign."""
        return self.session.query(OutreachDB).filter_by(campaign_id=campaign_id).all()

    def list_sent(self, limit: int = 100) -> list[OutreachDB]:
        """List sent outreaches."""
        return (
            self.session.query(OutreachDB)
            .filter(OutreachDB.status.in_(["sent", "opened", "replied"]))
            .order_by(OutreachDB.sent_at.desc())
            .limit(limit)
            .all()
        )

    def update_status(self, outreach_id: str, status: str, **kwargs) -> OutreachDB:
        """Update outreach status."""
        outreach = self.get_by_id(outreach_id)
        outreach.status = status
        for key, value in kwargs.items():
            if hasattr(outreach, key):
                setattr(outreach, key, value)
        return outreach


# Convenience functions
def investors(session: Session) -> InvestorRepository:
    return InvestorRepository(session)


def startups(session: Session) -> StartupRepository:
    return StartupRepository(session)


def campaigns(session: Session) -> CampaignRepository:
    return CampaignRepository(session)


def outreaches(session: Session) -> OutreachRepository:
    return OutreachRepository(session)


def funding_announcements(session: Session) -> list:
    """Query funding announcements."""
    return (
        session.query(FundingAnnouncementDB)
        .order_by(FundingAnnouncementDB.announcement_date.desc())
        .all()
    )
