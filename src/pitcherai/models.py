"""SQLAlchemy models for PitcherAI."""

from datetime import datetime, timezone
from uuid import UUID, uuid4
from typing import List, Optional, Dict, Any
from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    Boolean,
    JSON,
    Date,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pitcherai.database import Base


def uuid_pk() -> UUID:
    """Generate a UUID primary key."""
    return uuid4()


class TimestampMixin:
    """Mixin for created_at and updated_at timestamps."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )


class User(Base, TimestampMixin):
    """User/startup model."""

    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid_pk)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    startup_name: Mapped[str] = mapped_column(String(255), nullable=False)
    startup_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    niche: Mapped[str] = mapped_column(String(100), nullable=False)

    # Relationships
    campaigns: Mapped[List["Campaign"]] = relationship(
        "Campaign", back_populates="user"
    )


class Investor(Base, TimestampMixin):
    """Investor model (VC firm or individual angel)."""

    __tablename__ = "investors"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid_pk)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    investor_type: Mapped[str] = mapped_column(String(50), nullable=False)  # vc, angel
    firm_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    linkedin_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    focus_areas: Mapped[Optional[List[Any]]] = mapped_column(JSON, nullable=True)
    stage_preferences: Mapped[Optional[List[Any]]] = mapped_column(JSON, nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    source: Mapped[str] = mapped_column(String(100), nullable=False)
    raw_data: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)

    # Relationships
    investments: Mapped[List["Investment"]] = relationship(
        "Investment", back_populates="investor"
    )
    shared_connections: Mapped[List["SharedConnection"]] = relationship(
        "SharedConnection", back_populates="investor"
    )


class Investment(Base, TimestampMixin):
    """Track investments made by investors."""

    __tablename__ = "investments"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid_pk)
    investor_id: Mapped[UUID] = mapped_column(
        ForeignKey("investors.id"), nullable=False
    )
    startup_name: Mapped[str] = mapped_column(String(255), nullable=False)
    investment_date: Mapped[Optional[datetime]] = mapped_column(Date, nullable=True)
    round_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    amount_usd: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    source: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    raw_data: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)

    # Relationships
    investor: Mapped["Investor"] = relationship(
        "Investor", back_populates="investments"
    )


class SharedConnection(Base, TimestampMixin):
    """Shared connections between user and investor."""

    __tablename__ = "shared_connections"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid_pk)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    investor_id: Mapped[UUID] = mapped_column(
        ForeignKey("investors.id"), nullable=False
    )
    connection_name: Mapped[str] = mapped_column(String(255), nullable=False)
    connection_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    relationship_type: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Relationships
    investor: Mapped["Investor"] = relationship(
        "Investor", back_populates="shared_connections"
    )


class Template(Base, TimestampMixin):
    """Email template for campaigns."""

    __tablename__ = "templates"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid_pk)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    subject_template: Mapped[str] = mapped_column(Text, nullable=False)
    body_template: Mapped[str] = mapped_column(Text, nullable=False)
    variant_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relationships
    campaigns: Mapped[List["Campaign"]] = relationship(
        "Campaign", back_populates="template"
    )


class Campaign(Base, TimestampMixin):
    """Outreach campaign."""

    __tablename__ = "campaigns"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid_pk)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(
        String(50), default="draft"
    )  # draft, active, paused, completed
    template_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("templates.id"), nullable=True
    )
    target_criteria: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        JSON, nullable=True
    )
    started_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="campaigns")
    template: Mapped[Optional["Template"]] = relationship(
        "Template", back_populates="campaigns"
    )
    targets: Mapped[List["CampaignTarget"]] = relationship(
        "CampaignTarget", back_populates="campaign"
    )


class CampaignTarget(Base, TimestampMixin):
    """Target investor for a specific campaign."""

    __tablename__ = "campaign_targets"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid_pk)
    campaign_id: Mapped[UUID] = mapped_column(
        ForeignKey("campaigns.id"), nullable=False
    )
    investor_id: Mapped[UUID] = mapped_column(
        ForeignKey("investors.id"), nullable=False
    )
    status: Mapped[str] = mapped_column(
        String(50), default="pending"
    )  # pending, approved, rejected, sent
    email_subject: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    email_body: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    scheduled_send_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    sent_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    user_override_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    campaign: Mapped["Campaign"] = relationship("Campaign", back_populates="targets")
    investor: Mapped["Investor"] = relationship("Investor")
    tracking: Mapped[Optional["EmailTracking"]] = relationship(
        "EmailTracking", back_populates="campaign_target", uselist=False
    )


class EmailTracking(Base, TimestampMixin):
    """Track email opens, clicks, and replies."""

    __tablename__ = "email_tracking"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid_pk)
    campaign_target_id: Mapped[UUID] = mapped_column(
        ForeignKey("campaign_targets.id"), unique=True, nullable=False
    )
    message_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    opens_count: Mapped[int] = mapped_column(Integer, default=0)
    clicks_count: Mapped[int] = mapped_column(Integer, default=0)
    replied_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    bounced_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    last_opened_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    campaign_target: Mapped["CampaignTarget"] = relationship(
        "CampaignTarget", back_populates="tracking"
    )


class Analytics(Base, TimestampMixin):
    """Campaign analytics snapshot."""

    __tablename__ = "analytics"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid_pk)
    campaign_id: Mapped[UUID] = mapped_column(
        ForeignKey("campaigns.id"), nullable=False
    )
    date: Mapped[datetime] = mapped_column(Date, nullable=False)
    sent_count: Mapped[int] = mapped_column(Integer, default=0)
    open_count: Mapped[int] = mapped_column(Integer, default=0)
    click_count: Mapped[int] = mapped_column(Integer, default=0)
    reply_count: Mapped[int] = mapped_column(Integer, default=0)
    open_rate: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    reply_rate: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
