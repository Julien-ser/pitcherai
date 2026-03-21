"""FastAPI main application."""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from pitcherai.config import settings
from pitcherai.database import get_db, init_db, close_db
from pitcherai.models import User, Investor, Campaign, Template
from pitcherai.schemas import (
    UserCreate,
    UserUpdate,
    UserResponse,
    InvestorCreate,
    InvestorResponse,
    CampaignCreate,
    CampaignUpdate,
    CampaignResponse,
    TemplateCreate,
    TemplateUpdate,
    TemplateResponse,
    EmailGenerateRequest,
    EmailGenerateResponse,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events."""
    await init_db()
    yield
    await close_db()


app = FastAPI(
    title="PitcherAI API",
    description="AI-Powered autonomous VC outreach agent",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "timestamp": datetime.datetime.utcnow().isoformat()}


# Users
@app.post("/api/users", response_model=UserResponse)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """Create a new user."""
    # Implementation will be in crud.py
    raise NotImplementedError


@app.get("/api/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, db: AsyncSession = Depends(get_db)):
    """Get user by ID."""
    raise NotImplementedError


@app.put("/api/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str, user_update: UserUpdate, db: AsyncSession = Depends(get_db)
):
    """Update user."""
    raise NotImplementedError


# Investors
@app.get("/api/investors", response_model=list[InvestorResponse])
async def list_investors(
    skip: int = 0,
    limit: int = 100,
    investor_type: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    """List investors with optional filters."""
    raise NotImplementedError


@app.post("/api/investors", response_model=InvestorResponse)
async def create_investor(investor: InvestorCreate, db: AsyncSession = Depends(get_db)):
    """Create a new investor."""
    raise NotImplementedError


@app.get("/api/investors/{investor_id}", response_model=InvestorResponse)
async def get_investor(investor_id: str, db: AsyncSession = Depends(get_db)):
    """Get investor by ID."""
    raise NotImplementedError


# Templates
@app.get("/api/templates", response_model=list[TemplateResponse])
async def list_templates(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    """List email templates."""
    raise NotImplementedError


@app.post("/api/templates", response_model=TemplateResponse)
async def create_template(template: TemplateCreate, db: AsyncSession = Depends(get_db)):
    """Create a new template."""
    raise NotImplementedError


@app.put("/api/templates/{template_id}", response_model=TemplateResponse)
async def update_template(
    template_id: str,
    template_update: TemplateUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update template."""
    raise NotImplementedError


# Campaigns
@app.post("/api/campaigns", response_model=CampaignResponse)
async def create_campaign(campaign: CampaignCreate, db: AsyncSession = Depends(get_db)):
    """Create a new campaign."""
    raise NotImplementedError


@app.get("/api/campaigns", response_model=list[CampaignResponse])
async def list_campaigns(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    """List campaigns."""
    raise NotImplementedError


@app.get("/api/campaigns/{campaign_id}", response_model=CampaignResponse)
async def get_campaign(campaign_id: str, db: AsyncSession = Depends(get_db)):
    """Get campaign by ID."""
    raise NotImplementedError


# Email Generation
@app.post("/api/generate-email", response_model=EmailGenerateResponse)
async def generate_email(
    request: EmailGenerateRequest, db: AsyncSession = Depends(get_db)
):
    """Generate personalized email for an investor."""
    raise NotImplementedError


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.api_host, port=settings.api_port)
