"""SQLAlchemy database models for PitcheRai."""

from sqlalchemy import Column, String, Float, Boolean, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base


class InvestorDB(Base):
    """Investor database model."""

    __tablename__ = "investors"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    firm = Column(String, nullable=False)
    focus_areas = Column(JSON, default=list)  # List of strings
    stage_preference = Column(JSON, default=list)  # List of strings
    portfolio = Column(JSON, default=list)  # List of company names
    recent_investments = Column(JSON, default=list)  # List of investment descriptions
    connections = Column(JSON, default=list)  # List of shared connections
    location = Column(String, nullable=True)
    check_size_min = Column(Float, nullable=True)
    check_size_max = Column(Float, nullable=True)
    website = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    outreaches = relationship("OutreachDB", back_populates="investor")


class StartupDB(Base):
    """Startup database model."""

    __tablename__ = "startups"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    industry = Column(String, nullable=False)
    stage = Column(String, nullable=False)  # pre-seed, seed, series-a, etc.
    description = Column(Text, nullable=True)
    funding_needed = Column(Float, nullable=True)
    location = Column(String, nullable=True)
    website = Column(String, nullable=True)
    founders = Column(JSON, default=list)  # List of founder names/emails
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    campaigns = relationship("CampaignDB", back_populates="startup")
    outreaches = relationship(
        "OutreachDB", back_populates="startup", foreign_keys="OutreachDB.startup_id"
    )


class EmailTemplateDB(Base):
    """Email template database model."""

    __tablename__ = "email_templates"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    subject = Column(Text, nullable=False)
    body = Column(Text, nullable=False)
    variant = Column(String, nullable=False)  # warm_intro, cold_pitch, followup
    tone = Column(String, default="professional")
    performance_score = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    outreaches = relationship("OutreachDB", back_populates="template")


class OutreachDB(Base):
    """Outreach database model."""

    __tablename__ = "outreaches"

    id = Column(String, primary_key=True, index=True)
    campaign_id = Column(String, ForeignKey("campaigns.id"), nullable=False, index=True)
    investor_id = Column(String, ForeignKey("investors.id"), nullable=False, index=True)
    startup_id = Column(String, ForeignKey("startups.id"), nullable=False, index=True)
    template_id = Column(String, ForeignKey("email_templates.id"), nullable=True)
    subject = Column(Text, nullable=False)
    body = Column(Text, nullable=False)
    sent_at = Column(DateTime(timezone=True), nullable=True)
    status = Column(
        String, default="draft"
    )  # draft, queued, sent, opened, replied, bounced
    response = Column(Text, nullable=True)
    response_type = Column(
        String, nullable=True
    )  # interested, not_interested, maybe_later
    overridden = Column(Boolean, default=False)  # manually edited by user
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    campaign = relationship("CampaignDB", back_populates="outreaches")
    investor = relationship("InvestorDB", back_populates="outreaches")
    startup = relationship("StartupDB", back_populates="outreaches")
    template = relationship("EmailTemplateDB", back_populates="outreaches")


class CampaignDB(Base):
    """Campaign database model."""

    __tablename__ = "campaigns"

    id = Column(String, primary_key=True, index=True)
    startup_id = Column(String, ForeignKey("startups.id"), nullable=False, index=True)
    name = Column(String, nullable=False)
    target_criteria = Column(JSON, default=dict)  # filters for investor selection
    status = Column(String, default="draft")  # draft, active, paused, completed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    metrics = Column(JSON, default=dict)  # sent, opened, replied, etc.

    # Relationships
    startup = relationship("StartupDB", back_populates="campaigns")
    outreaches = relationship("OutreachDB", back_populates="campaign")
