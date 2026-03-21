"""Celery tasks for async email processing."""

import asyncio
from typing import Optional, List
from uuid import UUID

from celery import Celery
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..config import settings
from ..database import AsyncSessionLocal
from .. import crud
from ..services.email_generation import email_generator
from ..services.gmail import gmail_service


# Create Celery app
celery_app = Celery(
    "pitcherai",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
)


@celery_app.task(bind=True, name="send_single_email")
def send_single_email(
    self,
    target_id: str,
    subject: str,
    body: str,
    to_email: str,
):
    """Send a single email via Gmail API."""

    async def _send():
        async with AsyncSessionLocal() as db:
            # Mark target as sent
            target = await crud.campaign_target.get(db, id=UUID(target_id))
            if not target:
                return {"success": False, "error": "Target not found"}

            # Send email
            message_id = await gmail_service.send_email(
                to_email=to_email,
                subject=subject,
                body=body,
            )

            if message_id:
                # Update target as sent
                await crud.campaign_target.mark_sent(
                    db, target_id=UUID(target_id), message_id=message_id
                )
                # Create tracking record
                await crud.email_tracking.create(
                    db, target_id=UUID(target_id), message_id=message_id
                )
                await db.commit()
                return {"success": True, "message_id": message_id}
            else:
                return {"success": False, "error": "Failed to send email"}

    try:
        return asyncio.run(_send())
    except Exception as e:
        return {"success": False, "error": str(e)}


@celery_app.task(bind=True, name="generate_and_send_campaign_emails")
def generate_and_send_campaign_emails(
    self, campaign_id: str, send_immediately: bool = False
):
    """Generate emails for all targets in a campaign and optionally send them."""

    async def _process():
        async with AsyncSessionLocal() as db:
            campaign = await crud.campaign.get(db, id=UUID(campaign_id))
            if not campaign:
                return {"success": False, "error": "Campaign not found"}

            # Get template and user
            template = await crud.template.get(db, id=campaign.template_id)
            user = await crud.user.get(db, id=campaign.user_id)
            if not template or not user:
                return {"success": False, "error": "Missing template or user"}

            # Get pending targets
            targets = await crud.campaign_target.get_pending(
                db, campaign_id=UUID(campaign_id)
            )

            results = []
            for target in targets:
                investor = await crud.investor.get(db, id=target.investor_id)
                if not investor:
                    continue

                # Fetch recent investments
                result = await db.execute(
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
                    for inv in result.scalars().all()
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
                    )

                    # Update target
                    await crud.campaign_target.update(
                        db,
                        db_obj=target,
                        obj_in=crud.CampaignTargetUpdate(
                            email_subject=subject,
                            email_body=body,
                            status="approved" if send_immediately else "pending",
                        ),
                    )

                    # If sending immediately, queue email task
                    if send_immediately and investor.email:
                        send_single_email.delay(
                            target_id=str(target.id),
                            subject=subject,
                            body=body,
                            to_email=investor.email or "",
                        )

                    results.append({"target_id": str(target.id), "generated": True})

                except Exception as e:
                    results.append({"target_id": str(target.id), "error": str(e)})

            await db.commit()
            return {"success": True, "results": results, "total": len(targets)}

    try:
        return asyncio.run(_process())
    except Exception as e:
        return {"success": False, "error": str(e)}


@celery_app.task(bind=True, name="track_email_opens")
def track_email_opens(self, target_id: str):
    """Track email opens."""

    async def _track():
        async with AsyncSessionLocal() as db:
            await crud.email_tracking.update_open(db, target_id=UUID(target_id))
            await db.commit()
            return {"success": True}

    try:
        return asyncio.run(_track())
    except Exception as e:
        return {"success": False, "error": str(e)}


@celery_app.task(bind=True, name="track_email_replies")
def track_email_replies(self, target_id: str):
    """Track email replies."""

    async def _track():
        async with AsyncSessionLocal() as db:
            await crud.email_tracking.update_reply(db, target_id=UUID(target_id))
            await db.commit()
            return {"success": True}

    try:
        return asyncio.run(_track())
    except Exception as e:
        return {"success": False, "error": str(e)}
