"""SQLAlchemy database models."""

from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    Float,
    Integer,
    Boolean,
    DateTime,
    Text,
    JSON,
    ForeignKey,
    Enum as SQLEnum,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import func

Base = declarative_base()


class InvestorDB(Base):
    """Investor database model."""

    __tablename__ = "investors"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False, index=True)
    firm = Column(String, nullable=False, index=True)
    email = Column(String, unique=True, nullable=True, index=True)
    title = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    industry_focus = Column(JSON, default=list)  # List of industries
    investment_stage = Column(JSON, default=list)  # List of stages
    location = Column(String, nullable=True)
    website = Column(String, nullable=True)
    linkedin_url = Column(String, nullable=True, unique=True)
    connections = Column(JSON, default=list)  # List of connection objects
    portfolio_companies = Column(JSON, default=list)  # List of company objects
    metadata = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    outreaches = relationship("OutreachDB", back_populates="investor")


class StartupDB(Base):
    """Startup database model."""

    __tablename__ = "startups"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=False)
    industry = Column(String, nullable=False, index=True)
    stage = Column(String, nullable=False, index=True)  # pre-seed, seed, series a, etc.
    funding_goal = Column(Float, nullable=True)
    founders = Column(JSON, default=list)  # List of founder dicts
    website = Column(String, nullable=True)
    email = Column(String, nullable=True, index=True)
    location = Column(String, nullable=True)
    team_size = Column(Integer, nullable=True)
    revenue = Column(String, nullable=True)
    traction = Column(Text, nullable=True)
    metadata = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    campaigns = relationship("CampaignDB", back_populates="startup")


class CampaignDB(Base):
    """Campaign database model."""

    __tablename__ = "campaigns"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    startup_id = Column(String, ForeignKey("startups.id"), nullable=False, index=True)
    status = Column(
        String,
        nullable=False,
        default="draft",
        index=True,
    )  # draft, active, paused, completed
    target_criteria = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    metrics = Column(JSON, default=dict)

    # Relationships
    startup = relationship("StartupDB", back_populates="campaigns")
    outreaches = relationship("OutreachDB", back_populates="campaign")


class EmailTemplateDB(Base):
    """Email template database model."""

    __tablename__ = "email_templates"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    variant = Column(
        String, nullable=False, index=True
    )  # cold_pitch, warm_intro, follow_up
    subject = Column(Text, nullable=False)
    body = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    performance_score = Column(Float, default=0.0)
    usage_count = Column(Integer, default=0)
    success_rate = Column(Float, default=0.0)

    # Relationships
    outreaches = relationship("OutreachDB", back_populates="template")


class OutreachDB(Base):
    """Outreach database model."""

    __tablename__ = "outreaches"

    id = Column(String, primary_key=True)
    campaign_id = Column(String, ForeignKey("campaigns.id"), nullable=False, index=True)
    investor_id = Column(String, ForeignKey("investors.id"), nullable=False, index=True)
    template_id = Column(String, ForeignKey("email_templates.id"), nullable=False)
    subject = Column(Text, nullable=False)
    body = Column(Text, nullable=False)
    status = Column(
        String, nullable=False, default="draft", index=True
    )  # draft, scheduled, sent, opened, replied, bounced
    sent_at = Column(DateTime(timezone=True), nullable=True, index=True)
    opened_at = Column(DateTime(timezone=True), nullable=True)
    replied_at = Column(DateTime(timezone=True), nullable=True, index=True)
    response_type = Column(
        String, nullable=True
    )  # interested, not_interested, maybe_later
    response_snippet = Column(Text, nullable=True)
    metadata = Column(JSON, default=dict)

    # Relationships
    campaign = relationship("CampaignDB", back_populates="outreaches")
    investor = relationship("InvestorDB", back_populates="outreaches")
    template = relationship("EmailTemplateDB", back_populates="outreaches")


class FundingAnnouncementDB(Base):
    """Funding announcement database model."""

    __tablename__ = "funding_announcements"

    id = Column(String, primary_key=True)
    source = Column(String, nullable=False, index=True)  # crunchbase, angellist, rss
    company_name = Column(String, nullable=False, index=True)
    company_url = Column(String, nullable=True)
    funding_amount = Column(Float, nullable=True)
    funding_round = Column(String, nullable=True)
    announcement_date = Column(DateTime(timezone=True), nullable=False, index=True)
    investors = Column(JSON, default=list)  # List of investor IDs/names
    industry = Column(String, nullable=True, index=True)
    stage = Column(String, nullable=True, index=True)
    metadata = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


def init_db(engine):
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)


def get_sessionmaker(engine):
    """Get session factory."""
    return sessionmaker(bind=engine, autocommit=False, autoflush=False)
