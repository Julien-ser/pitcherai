"""Pydantic models for data validation."""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, EmailStr, Field


class Investor(BaseModel):
    """Investor model."""

    id: str
    name: str
    firm: str
    email: Optional[EmailStr] = None
    title: Optional[str] = None
    bio: Optional[str] = None
    industry_focus: List[str] = Field(default_factory=list)
    investment_stage: List[str] = Field(default_factory=list)
    location: Optional[str] = None
    website: Optional[str] = None
    linkedin_url: Optional[str] = None
    connections: List[Dict[str, Any]] = Field(default_factory=list)
    portfolio_companies: List[Dict[str, Any]] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def dict(self, **kwargs):
        return super().dict(**kwargs)


class Startup(BaseModel):
    """Startup profile model."""

    id: str
    name: str
    description: str
    industry: str
    stage: str  # pre-seed, seed, series a, etc.
    funding_goal: Optional[float] = None
    founders: List[Dict[str, str]] = Field(default_factory=list)
    website: Optional[str] = None
    email: Optional[EmailStr] = None
    location: Optional[str] = None
    team_size: Optional[int] = None
    revenue: Optional[str] = None
    traction: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def dict(self, **kwargs):
        return super().dict(**kwargs)


class Campaign(BaseModel):
    """Campaign model."""

    id: str
    name: str
    startup_id: str
    status: str = "draft"  # draft, active, paused, completed
    target_criteria: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    targets: List[str] = Field(default_factory=list)  # investor IDs
    metrics: Dict[str, Any] = Field(default_factory=dict)

    def dict(self, **kwargs):
        return super().dict(**kwargs)


class EmailTemplate(BaseModel):
    """Email template model."""

    id: str
    name: str
    variant: str  # cold_pitch, warm_intro, follow_up
    subject: str
    body: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    performance_score: float = 0.0
    usage_count: int = 0
    success_rate: float = 0.0

    def dict(self, **kwargs):
        return super().dict(**kwargs)


class Outreach(BaseModel):
    """Outreach record model."""

    id: str
    campaign_id: str
    investor_id: str
    template_id: str
    subject: str
    body: str
    status: str = "draft"  # draft, scheduled, sent, opened, replied, bounced
    sent_at: Optional[datetime] = None
    opened_at: Optional[datetime] = None
    replied_at: Optional[datetime] = None
    response_type: Optional[str] = None  # interested, not_interested, maybe_later
    response_snippet: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def dict(self, **kwargs):
        return super().dict(**kwargs)


class FundingAnnouncement(BaseModel):
    """Funding announcement model."""

    id: str
    source: str  # crunchbase, angellist, rss
    company_name: str
    company_url: Optional[str] = None
    funding_amount: Optional[float] = None
    funding_round: Optional[str] = None
    announcement_date: datetime
    investors: List[str] = Field(default_factory=list)
    industry: Optional[str] = None
    stage: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def dict(self, **kwargs):
        return super().dict(**kwargs)
