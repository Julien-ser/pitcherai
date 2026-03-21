"""FastAPI main application."""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone

from .config import settings
from .database import get_db, init_db, close_db
from . import crud
from .models import Investment
from .services.email_generation import email_generator
from .services.campaign import campaign_service
from .services.prospecting import prospecting_service
from .schemas import (
    UserCreate,
    UserUpdate,
    UserResponse,
    InvestorCreate,
    InvestorUpdate,
    InvestorResponse,
    TemplateCreate,
    TemplateUpdate,
    TemplateResponse,
    CampaignCreate,
    CampaignUpdate,
    CampaignResponse,
    CampaignTargetCreate,
    CampaignTargetUpdate,
    CampaignTargetResponse,
    EmailGenerateRequest,
    EmailGenerateResponse,
    AnalyticsResponse,
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
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}


# Users
@app.post(
    "/api/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """Create a new user."""
    existing = await crud.user.get_by_email(db, email=user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.user.create(db, obj_in=user)


@app.get("/api/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, db: AsyncSession = Depends(get_db)):
    """Get user by ID."""
    from uuid import UUID

    try:
        uid = UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID")
    user = await crud.user.get(db, id=uid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.put("/api/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str, user_update: UserUpdate, db: AsyncSession = Depends(get_db)
):
    """Update user."""
    from uuid import UUID

    try:
        uid = UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID")
    user = await crud.user.get(db, id=uid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return await crud.user.update(db, db_obj=user, obj_in=user_update)


# Investors
@app.get("/api/investors", response_model=list[InvestorResponse])
async def list_investors(
    skip: int = 0,
    limit: int = 100,
    investor_type: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    """List investors with optional filters."""
    if investor_type:
        return await crud.investor.list_by_type(
            db, investor_type=investor_type, skip=skip, limit=limit
        )
    return await crud.investor.get_multi(db, skip=skip, limit=limit)


@app.post(
    "/api/investors",
    response_model=InvestorResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_investor(investor: InvestorCreate, db: AsyncSession = Depends(get_db)):
    """Create a new investor."""
    return await crud.investor.create(db, obj_in=investor)


@app.get("/api/investors/{investor_id}", response_model=InvestorResponse)
async def get_investor(investor_id: str, db: AsyncSession = Depends(get_db)):
    """Get investor by ID."""
    from uuid import UUID

    try:
        iid = UUID(investor_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid investor ID")
    investor = await crud.investor.get(db, id=iid)
    if not investor:
        raise HTTPException(status_code=404, detail="Investor not found")
    return investor


@app.get("/api/investors/{investor_id}/investments")
async def get_investor_investments(
    investor_id: str, db: AsyncSession = Depends(get_db)
):
    """Get portfolio investments for an investor."""
    from uuid import UUID

    try:
        iid = UUID(investor_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid investor ID")
    investor = await crud.investor.get(db, id=iid)
    if not investor:
        raise HTTPException(status_code=404, detail="Investor not found")
    return {"investor_id": investor_id, "investments": investor.investments}


# Templates
@app.get("/api/templates", response_model=list[TemplateResponse])
async def list_templates(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = False,
    db: AsyncSession = Depends(get_db),
):
    """List email templates."""
    if active_only:
        return await crud.template.get_active(db)
    return await crud.template.get_multi(db, skip=skip, limit=limit)


@app.post(
    "/api/templates",
    response_model=TemplateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_template(template: TemplateCreate, db: AsyncSession = Depends(get_db)):
    """Create a new template."""
    return await crud.template.create(db, obj_in=template)


@app.put("/api/templates/{template_id}", response_model=TemplateResponse)
async def update_template(
    template_id: str,
    template_update: TemplateUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update template."""
    from uuid import UUID

    try:
        tid = UUID(template_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid template ID")
    template = await crud.template.get(db, id=tid)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return await crud.template.update(db, db_obj=template, obj_in=template_update)


# Campaigns
@app.post(
    "/api/campaigns",
    response_model=CampaignResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_campaign(campaign: CampaignCreate, db: AsyncSession = Depends(get_db)):
    """Create a new campaign."""
    return await crud.campaign.create(db, obj_in=campaign)


@app.get("/api/campaigns", response_model=list[CampaignResponse])
async def list_campaigns(
    skip: int = 0,
    limit: int = 100,
    user_id: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    """List campaigns."""
    if user_id:
        from uuid import UUID

        try:
            uid = UUID(user_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid user ID")
        return await crud.campaign.get_by_user(db, user_id=uid, skip=skip, limit=limit)
    return await crud.campaign.get_multi(db, skip=skip, limit=limit)


@app.get("/api/campaigns/{campaign_id}", response_model=CampaignResponse)
async def get_campaign(campaign_id: str, db: AsyncSession = Depends(get_db)):
    """Get campaign by ID."""
    from uuid import UUID

    try:
        cid = UUID(campaign_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid campaign ID")
    campaign = await crud.campaign.get(db, id=cid)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign


@app.put("/api/campaigns/{campaign_id}", response_model=CampaignResponse)
async def update_campaign(
    campaign_id: str,
    campaign_update: CampaignUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update campaign."""
    from uuid import UUID

    try:
        cid = UUID(campaign_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid campaign ID")
    campaign = await crud.campaign.get(db, id=cid)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return await crud.campaign.update(db, db_obj=campaign, obj_in=campaign_update)


@app.post("/api/campaigns/{campaign_id}/start", response_model=CampaignResponse)
async def start_campaign(campaign_id: str, db: AsyncSession = Depends(get_db)):
    """Start a campaign."""
    from uuid import UUID

    try:
        cid = UUID(campaign_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid campaign ID")
    campaign = await campaign_service.start_campaign(db, cid)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign


@app.post("/api/campaigns/{campaign_id}/pause", response_model=CampaignResponse)
async def pause_campaign(campaign_id: str, db: AsyncSession = Depends(get_db)):
    """Pause a campaign."""
    from uuid import UUID

    try:
        cid = UUID(campaign_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid campaign ID")
    campaign = await crud.campaign.get(db, id=cid)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    update = CampaignUpdate(status="paused")
    return await crud.campaign.update(db, db_obj=campaign, obj_in=update)


@app.get("/api/campaigns/{campaign_id}/targets")
async def get_campaign_targets(campaign_id: str, db: AsyncSession = Depends(get_db)):
    """Get campaign targets."""
    from uuid import UUID

    try:
        cid = UUID(campaign_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid campaign ID")
    targets = await crud.campaign_target.get_by_campaign(db, campaign_id=cid)
    return {"campaign_id": campaign_id, "targets": targets}


# Email Generation
@app.post("/api/generate-email", response_model=EmailGenerateResponse)
async def generate_email(
    request: EmailGenerateRequest, db: AsyncSession = Depends(get_db)
):
    """Generate personalized email for an investor."""
    # Get investor
    investor = await crud.investor.get(db, id=request.investor_id)
    if not investor:
        raise HTTPException(status_code=404, detail="Investor not found")

    # Get template
    template = await crud.template.get(db, id=request.template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    # Get user
    user = await crud.user.get(db, id=request.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get investor's recent investments
    investments = await db.execute(
        select(crud.models.Investment)
        .where(crud.models.Investment.investor_id == investor.id)
        .order_by(crud.models.Investment.investment_date.desc())
        .limit(5)
    )
    recent_investments = [
        {
            "startup_name": inv.startup_name,
            "round_type": inv.round_type,
            "investment_date": inv.investment_date.isoformat()
            if inv.investment_date
            else None,
        }
        for inv in investments.scalars().all()
    ]

    # Generate email
    try:
        subject, body = await email_generator.generate_email(
            investor_name=investor.name,
            investor_firm=investor.firm_name,
            investor_focus=investor.focus_areas,
            investor_recent_investments=recent_investments,
            user_startup=user.startup_name,
            user_description=user.startup_description or "",
            user_niche=user.niche,
            template_subject=template.subject_template,
            template_body=template.body_template,
            custom_vars=request.custom_vars,
        )
        return EmailGenerateResponse(subject=subject, body=body)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Email generation failed: {str(e)}"
        )


@app.post("/api/generate-campaign-emails")
async def generate_campaign_emails(
    campaign_id: str, db: AsyncSession = Depends(get_db)
):
    """Generate emails for all pending targets in a campaign."""
    from uuid import UUID

    try:
        cid = UUID(campaign_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid campaign ID")
    await campaign_service._generate_emails_for_campaign(db, cid)
    return {"message": "Emails generated successfully", "campaign_id": campaign_id}


# Prospecting
@app.post("/api/prospecting/import")
async def import_investors(
    queries: list[str] = [],
    sources: list[str] = ["crunchbase", "angellist"],
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
):
    """Import investors from external sources."""
    count = await prospecting_service.import_investors_from_sources(
        db, queries=queries, sources=sources, limit_per_source=limit
    )
    return {"imported_count": count}


@app.post("/api/prospecting/enrich/{investor_id}")
async def enrich_investor_portfolio(
    investor_id: str, db: AsyncSession = Depends(get_db)
):
    """Enrich an investor's portfolio with recent investments."""
    from uuid import UUID

    try:
        iid = UUID(investor_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid investor ID")
    count = await prospecting_service.enrich_investor_portfolio(db, investor_id=iid)
    return {"investor_id": investor_id, "investments_added": count}


# Campaign Targets
@app.post("/api/campaigns/{campaign_id}/targets", response_model=CampaignTargetResponse)
async def add_campaign_target(
    campaign_id: str,
    target: CampaignTargetCreate,
    db: AsyncSession = Depends(get_db),
):
    """Add a target to a campaign."""
    from uuid import UUID

    try:
        cid = UUID(campaign_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid campaign ID")

    # Verify campaign exists
    campaign = await crud.campaign.get(db, id=cid)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    # Override campaign_id in the target
    target_data = target.model_dump()
    target_data["campaign_id"] = cid
    target_create = CampaignTargetCreate(**target_data)

    return await crud.campaign_target.create(db, obj_in=target_create)


@app.get(
    "/api/campaigns/{campaign_id}/targets", response_model=list[CampaignTargetResponse]
)
async def list_campaign_targets(
    campaign_id: str,
    status: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    """List targets for a campaign with optional filter."""
    from uuid import UUID

    try:
        cid = UUID(campaign_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid campaign ID")

    if status:
        # Filter by status would need custom query
        targets = await crud.campaign_target.get_by_campaign(db, campaign_id=cid)
        return [t for t in targets if t.status == status]
    return await crud.campaign_target.get_by_campaign(db, campaign_id=cid)


@app.put("/api/campaign-targets/{target_id}", response_model=CampaignTargetResponse)
async def update_campaign_target(
    target_id: str,
    target_update: CampaignTargetUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update a campaign target."""
    from uuid import UUID

    try:
        tid = UUID(target_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid target ID")
    target = await crud.campaign_target.get(db, id=tid)
    if not target:
        raise HTTPException(status_code=404, detail="Target not found")
    return await crud.campaign_target.update(db, db_obj=target, obj_in=target_update)


@app.delete("/api/campaign-targets/{target_id}")
async def delete_campaign_target(target_id: str, db: AsyncSession = Depends(get_db)):
    """Delete a campaign target."""
    from uuid import UUID

    try:
        tid = UUID(target_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid target ID")
    success = await crud.campaign_target.delete(db, id=tid)
    if not success:
        raise HTTPException(status_code=404, detail="Target not found")
    return {"deleted": True}


# Email Tracking
@app.get("/api/tracking")
async def list_email_tracking(
    campaign_id: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    """List email tracking records."""
    from uuid import UUID

    if campaign_id:
        try:
            cid = UUID(campaign_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid campaign ID")
        # Get all targets for campaign
        targets = await crud.campaign_target.get_by_campaign(db, campaign_id=cid)
        result = []
        for target in targets:
            tracking = await crud.email_tracking.get_by_target(db, target_id=target.id)
            if tracking:
                result.append(
                    {
                        "target_id": str(target.id),
                        "investor_name": target.investor.name,
                        "opens_count": tracking.opens_count,
                        "replied_at": tracking.replied_at.isoformat()
                        if tracking.replied_at
                        else None,
                        "last_opened_at": tracking.last_opened_at.isoformat()
                        if tracking.last_opened_at
                        else None,
                    }
                )
        return {"campaign_id": campaign_id, "tracking": result}
    return {"message": "Specify campaign_id to get tracking data"}


@app.post("/api/tracking/{target_id}/opens")
async def track_email_open(target_id: str, db: AsyncSession = Depends(get_db)):
    """Track email open (for webhook/pixel tracking)."""
    from uuid import UUID

    try:
        tid = UUID(target_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid target ID")
    tracking = await crud.email_tracking.update_open(db, target_id=tid)
    await db.commit()
    if not tracking:
        raise HTTPException(status_code=404, detail="Tracking record not found")
    return {"tracked": True, "opens_count": tracking.opens_count}


@app.post("/api/tracking/{target_id}/replies")
async def track_email_reply(target_id: str, db: AsyncSession = Depends(get_db)):
    """Track email reply (for webhook)."""
    from uuid import UUID

    try:
        tid = UUID(target_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid target ID")
    tracking = await crud.email_tracking.update_reply(db, target_id=tid)
    await db.commit()
    if not tracking:
        raise HTTPException(status_code=404, detail="Tracking record not found")
    return {"tracked": True, "replied_at": tracking.replied_at.isoformat()}


# Analytics
@app.get("/api/analytics/campaign/{campaign_id}")
async def get_campaign_analytics(campaign_id: str, db: AsyncSession = Depends(get_db)):
    """Get analytics for a campaign."""
    from uuid import UUID
    from datetime import date

    try:
        cid = UUID(campaign_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid campaign ID")

    # Calculate latest analytics
    targets = await crud.campaign_target.get_by_campaign(db, campaign_id=cid)
    sent_count = len([t for t in targets if t.status == "sent"])

    # Get tracking data
    open_count = 0
    reply_count = 0
    for target in targets:
        tracking = await crud.email_tracking.get_by_target(db, target_id=target.id)
        if tracking:
            open_count += tracking.opens_count
            if tracking.replied_at:
                reply_count += 1

    open_rate = (open_count / sent_count * 100) if sent_count > 0 else 0
    reply_rate = (reply_count / sent_count * 100) if sent_count > 0 else 0

    # Save to analytics table
    today = date.today()
    analytics = await crud.analytics.create_or_update(
        db,
        campaign_id=cid,
        date_val=today,
        sent_count=sent_count,
        open_count=open_count,
        reply_count=reply_count,
    )

    return {
        "campaign_id": campaign_id,
        "date": today.isoformat(),
        "sent_count": sent_count,
        "open_count": open_count,
        "reply_count": reply_count,
        "open_rate": round(open_rate, 2),
        "reply_rate": round(reply_rate, 2),
    }


@app.get("/api/analytics/dashboard")
async def get_dashboard_analytics(db: AsyncSession = Depends(get_db)):
    """Get overall dashboard analytics."""
    campaigns = await crud.campaign.get_multi(db, limit=100)

    total_campaigns = len(campaigns)
    total_sent = 0
    total_opens = 0
    total_replies = 0

    for campaign in campaigns:
        targets = await crud.campaign_target.get_by_campaign(
            db, campaign_id=campaign.id
        )
        for target in targets:
            if target.status == "sent":
                total_sent += 1
                tracking = await crud.email_tracking.get_by_target(
                    db, target_id=target.id
                )
                if tracking:
                    total_opens += tracking.opens_count
                    if tracking.replied_at:
                        total_replies += 1

    overall_open_rate = (total_opens / total_sent * 100) if total_sent > 0 else 0
    overall_reply_rate = (total_replies / total_sent * 100) if total_sent > 0 else 0

    return {
        "total_campaigns": total_campaigns,
        "total_sent_emails": total_sent,
        "total_opens": total_opens,
        "total_replies": total_replies,
        "overall_open_rate": round(overall_open_rate, 2),
        "overall_reply_rate": round(overall_reply_rate, 2),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.api_host, port=settings.api_port)
