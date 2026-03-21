"""Database models using SQLAlchemy"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Enum as SQLEnum,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import enum

Base = declarative_base()


class InvestorStatus(enum.Enum):
    """Status of an investor in the system"""

    PROSPECT = "prospect"
    CONTACTED = "contacted"
    REPLIED = "replied"
    INTERESTED = "interested"
    NOT_INTERESTED = "not_interested"
    ARCHIVED = "archived"


class EmailStatus(enum.Enum):
    """Status of an email"""

    DRAFT = "draft"
    SENT = "sent"
    DELIVERED = "delivered"
    OPENED = "opened"
    REPLIED = "replied"
    BOUNCED = "bounced"
    FAILED = "failed"


class TemplateStatus(enum.Enum):
    """Status of an email template"""

    ACTIVE = "active"
    INACTIVE = "inactive"
    TESTING = "testing"


class Investor(Base):
    """Represents a VC/angel investor"""

    __tablename__ = "investors"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), unique=True, nullable=True)
    firm = Column(String(200), nullable=True)
    title = Column(String(200), nullable=True)
    linkedin_url = Column(String(500), nullable=True)
    crunchbase_url = Column(String(500), nullable=True)
    angellist_url = Column(String(500), nullable=True)

    # Scoring
    relevance_score = Column(Float, default=0.0)
    last_funding_date = Column(DateTime, nullable=True)
    investment_stage = Column(String(100), nullable=True)
    investment_amount = Column(String(100), nullable=True)
    focus_areas = Column(Text, nullable=True)  # JSON string

    # Metadata
    status = Column(SQLEnum(InvestorStatus), default=InvestorStatus.PROSPECT)
    source = Column(String(100), nullable=True)
    source_url = Column(String(500), nullable=True)
    discovered_at = Column(DateTime, default=datetime.utcnow)
    last_contacted_at = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)

    # Relationships
    emails = relationship("Email", back_populates="investor")
    campaigns = relationship("CampaignInvestor", back_populates="investor")

    def __repr__(self):
        return f"<Investor(id={self.id}, name='{self.name}', email='{self.email}')>"


class EmailTemplate(Base):
    """Represents an email template"""

    __tablename__ = "templates"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    subject = Column(String(500), nullable=False)
    body = Column(Text, nullable=False)
    version = Column(Integer, default=1)
    status = Column(SQLEnum(TemplateStatus), default=TemplateStatus.ACTIVE)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Performance metrics
    sent_count = Column(Integer, default=0)
    open_rate = Column(Float, default=0.0)
    reply_rate = Column(Float, default=0.0)
    conversion_rate = Column(Float, default=0.0)

    # Relationships
    emails = relationship("Email", back_populates="template")

    def __repr__(self):
        return f"<EmailTemplate(id={self.id}, name='{self.name}')>"


class Email(Base):
    """Represents a sent or drafted email"""

    __tablename__ = "emails"

    id = Column(Integer, primary_key=True)
    investor_id = Column(Integer, ForeignKey("investors.id"), nullable=False)
    template_id = Column(Integer, ForeignKey("templates.id"), nullable=True)

    subject = Column(String(500), nullable=False)
    body = Column(Text, nullable=False)
    drafted_at = Column(DateTime, default=datetime.utcnow)
    sent_at = Column(DateTime, nullable=True)

    # Status tracking
    status = Column(SQLEnum(EmailStatus), default=EmailStatus.DRAFT)
    message_id = Column(String(200), nullable=True)  # Gmail message ID

    # Engagement metrics
    opened_at = Column(DateTime, nullable=True)
    replied_at = Column(DateTime, nullable=True)
    clicks = Column(Integer, default=0)

    # AI-generated fields
    personalization_notes = Column(Text, nullable=True)
    confidence_score = Column(Float, default=0.0)

    # Relationships
    investor = relationship("Investor", back_populates="emails")
    template = relationship("EmailTemplate", back_populates="emails")

    def __repr__(self):
        return f"<Email(id={self.id}, status='{self.status.value}')>"


class Campaign(Base):
    """Represents an outreach campaign"""

    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    target_criteria = Column(Text, nullable=True)  # JSON string of filters

    status = Column(String(50), default="active")
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)

    # Metrics
    total_investors = Column(Integer, default=0)
    emails_sent = Column(Integer, default=0)
    open_rate = Column(Float, default=0.0)
    reply_rate = Column(Float, default=0.0)

    # Relationships
    investors = relationship("CampaignInvestor", back_populates="campaign")

    def __repr__(self):
        return f"<Campaign(id={self.id}, name='{self.name}')>"


class CampaignInvestor(Base):
    """Association table for campaign-investor relationships"""

    __tablename__ = "campaign_investors"

    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    investor_id = Column(Integer, ForeignKey("investors.id"), nullable=False)
    added_at = Column(DateTime, default=datetime.utcnow)
    email_id = Column(Integer, ForeignKey("emails.id"), nullable=True)

    status = Column(SQLEnum(EmailStatus), default=EmailStatus.DRAFT)

    # Relationships
    campaign = relationship("Campaign", back_populates="investors")
    investor = relationship("Investor", back_populates="campaigns")

    def __repr__(self):
        return f"<CampaignInvestor(campaign_id={self.campaign_id}, investor_id={self.investor_id})>"


class LearningMetric(Base):
    """Stores learning metrics for template optimization"""

    __tablename__ = "learning_metrics"

    id = Column(Integer, primary_key=True)
    template_id = Column(Integer, ForeignKey("templates.id"), nullable=False)
    investor_id = Column(Integer, ForeignKey("investors.id"), nullable=False)
    email_id = Column(Integer, ForeignKey("emails.id"), nullable=False)

    # Features
    investor_relevance = Column(Float, default=0.0)
    personalization_score = Column(Float, default=0.0)
    investment_match = Column(Float, default=0.0)

    # Outcomes
    opened = Column(Boolean, default=False)
    replied = Column(Boolean, default=False)
    clicked = Column(Boolean, default=False)

    recorded_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<LearningMetric(id={self.id}, opened={self.opened}, replied={self.replied})>"
