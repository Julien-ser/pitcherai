"""Pydantic schemas for request/response validation."""

from datetime import datetime
from typing import Literal, Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    email: EmailStr
    startup_name: str
    startup_description: Optional[str] = None
    niche: str


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    startup_name: Optional[str] = None
    startup_description: Optional[str] = None
    niche: Optional[str] = None


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime


class InvestorBase(BaseModel):
    name: str
    investor_type: Literal["vc", "angel"]
    firm_name: Optional[str] = None
    email: Optional[EmailStr] = None
    linkedin_url: Optional[str] = None
    focus_areas: Optional[list] = None
    stage_preferences: Optional[list] = None
    location: Optional[str] = None


class InvestorCreate(InvestorBase):
    source: str
    raw_data: Optional[dict] = None


class InvestorResponse(InvestorBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    source: str
    created_at: datetime
    updated_at: datetime


class TemplateBase(BaseModel):
    name: str
    subject_template: str
    body_template: str
    variant_id: Optional[str] = None
    is_active: bool = True


class TemplateCreate(TemplateBase):
    pass


class TemplateUpdate(BaseModel):
    name: Optional[str] = None
    subject_template: Optional[str] = None
    body_template: Optional[str] = None
    variant_id: Optional[str] = None
    is_active: Optional[bool] = None


class TemplateResponse(TemplateBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime


class CampaignBase(BaseModel):
    name: str
    user_id: UUID
    template_id: Optional[UUID] = None
    target_criteria: Optional[dict] = None


class CampaignCreate(CampaignBase):
    pass


class CampaignUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[Literal["draft", "active", "paused", "completed"]] = None
    template_id: Optional[UUID] = None
    target_criteria: Optional[dict] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class CampaignResponse(CampaignBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    status: str
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class CampaignTargetBase(BaseModel):
    campaign_id: UUID
    investor_id: UUID
    status: Literal["pending", "approved", "rejected", "sent"] = "pending"
    email_subject: Optional[str] = None
    email_body: Optional[str] = None
    scheduled_send_at: Optional[datetime] = None
    user_override_notes: Optional[str] = None


class CampaignTargetCreate(CampaignTargetBase):
    pass


class CampaignTargetUpdate(BaseModel):
    status: Optional[Literal["pending", "approved", "rejected", "sent"]] = None
    email_subject: Optional[str] = None
    email_body: Optional[str] = None
    scheduled_send_at: Optional[datetime] = None
    user_override_notes: Optional[str] = None


class CampaignTargetResponse(CampaignTargetBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    sent_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class EmailGenerateRequest(BaseModel):
    investor_id: UUID
    template_id: UUID
    user_id: UUID
    custom_vars: Optional[dict] = None


class EmailGenerateResponse(BaseModel):
    subject: str
    body: str


class AnalyticsResponse(BaseModel):
    campaign_id: UUID
    date: datetime
    sent_count: int
    open_count: int
    click_count: int
    reply_count: int
    open_rate: Optional[float]
    reply_rate: Optional[float]

    model_config = ConfigDict(from_attributes=True)
