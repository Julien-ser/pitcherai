"""Core Pydantic data models for PitcheRai."""

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class Investor(BaseModel):
    """Investor/VC model."""

    id: str
    name: str
    email: EmailStr
    firm: str
    focus_areas: list[str] = Field(default_factory=list)
    stage_preference: list[str] = Field(default_factory=list)
    portfolio: list[str] = Field(default_factory=list)  # Company names
    recent_investments: list[str] = Field(default_factory=list)
    connections: list[str] = Field(default_factory=list)  # Shared connections
    location: str | None = None
    check_size_min: float | None = None
    check_size_max: float | None = None
    website: str | None = None


class Startup(BaseModel):
    """Startup profile model."""

    id: str
    name: str
    industry: str
    stage: str  # pre-seed, seed, series-a, etc.
    description: str
    funding_needed: float
    location: str | None = None
    website: str | None = None
    founders: list[str] = Field(default_factory=list)


class EmailTemplate(BaseModel):
    """Email template model."""

    id: str
    name: str
    subject: str
    body: str
    variant: str  # e.g., "warm_intro", "cold_pitch", "followup"
    tone: str = "professional"
    performance_score: float = 0.0


class Outreach(BaseModel):
    """Individual outreach attempt."""

    id: str
    campaign_id: str
    investor_id: str
    template_id: str | None = None
    subject: str
    body: str
    sent_at: datetime | None = None
    status: str = "draft"  # draft, queued, sent, opened, replied, bounced
    response: str | None = None
    response_type: str | None = None  # interested, not_interested, maybe_later
    overridden: bool = False  # manually edited by user


class Campaign(BaseModel):
    """Outreach campaign model."""

    id: str
    startup_id: str
    name: str
    target_criteria: dict  # filters for investor selection
    status: str = "draft"  # draft, active, paused, completed
    created_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: datetime | None = None
    completed_at: datetime | None = None
    targets: list[str] = Field(default_factory=list)  # investor_ids
    metrics: dict = Field(default_factory=dict)  # sent, opened, replied, etc.
