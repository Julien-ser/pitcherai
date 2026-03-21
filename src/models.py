"""Core Pydantic data models for PitcheRai."""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field


class Investor(BaseModel):
    """Investor/VC model."""

    id: str
    name: str
    email: EmailStr
    firm: str
    focus_areas: List[str] = Field(default_factory=list)
    stage_preference: List[str] = Field(default_factory=list)
    portfolio: List[str] = Field(default_factory=list)  # Company names
    recent_investments: List[str] = Field(default_factory=list)
    connections: List[str] = Field(default_factory=list)  # Shared connections
    location: Optional[str] = None
    check_size_min: Optional[float] = None
    check_size_max: Optional[float] = None
    website: Optional[str] = None


class Startup(BaseModel):
    """Startup profile model."""

    id: str
    name: str
    industry: str
    stage: str  # pre-seed, seed, series-a, etc.
    description: str
    funding_needed: float
    location: Optional[str] = None
    website: Optional[str] = None
    founders: List[str] = Field(default_factory=list)


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
    template_id: Optional[str] = None
    subject: str
    body: str
    sent_at: Optional[datetime] = None
    status: str = "draft"  # draft, queued, sent, opened, replied, bounced
    response: Optional[str] = None
    response_type: Optional[str] = None  # interested, not_interested, maybe_later
    overridden: bool = False  # manually edited by user


class Campaign(BaseModel):
    """Outreach campaign model."""

    id: str
    startup_id: str
    name: str
    target_criteria: dict  # filters for investor selection
    status: str = "draft"  # draft, active, paused, completed
    created_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    targets: List[str] = Field(default_factory=list)  # investor_ids
    metrics: dict = Field(default_factory=dict)  # sent, opened, replied, etc.
