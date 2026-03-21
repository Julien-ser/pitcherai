"""Campaign management service."""

from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from .. import crud
from .email_generation import email_generator
from ..models import CampaignTarget, Investor, User, Template


class CampaignService:
    """Service for managing outreach campaigns."""

    def __init__(self):
        pass

    async def create_campaign_with_targets(
        self,
        session: AsyncSession,
        name: str,
        user_id: UUID,
        template_id: UUID,
        target_criteria: Dict[str, Any],
        auto_generate_emails: bool = True,
    ) -> Campaign:
        """
        Create a new campaign and populate it with targets based on criteria.

        Args:
            session: Database session
            name: Campaign name
            user_id: User who owns the campaign
            template_id: Email template to use
            target_criteria: Dict with filters like:
                - investor_types: list of ["vc", "angel"]
                - focus_areas: list of sectors
                - min_stage: minimum investment stage
                - location: geographic preference
            auto_generate_emails: Whether to generate emails for targets immediately

        Returns:
            Created Campaign object
        """
        # Create campaign
        campaign = await crud.campaign.create(
            session,
            obj_in=CampaignCreate(
                name=name,
                user_id=user_id,
                template_id=template_id,
                target_criteria=target_criteria,
                status="draft",
            ),
        )

        # Find matching investors
        investors = await self._find_matching_investors(session, target_criteria)

        # Create campaign targets
        for investor in investors:
            await crud.campaign_target.create(
                session,
                obj_in=CampaignTargetCreate(
                    campaign_id=campaign.id,
                    investor_id=investor.id,
                    status="pending",
                ),
            )

        # Optionally generate emails for targets
        if auto_generate_emails:
            await self._generate_emails_for_campaign(session, campaign.id)

        return campaign

    async def _find_matching_investors(
        self, session: AsyncSession, criteria: Dict[str, Any]
    ) -> List[Investor]:
        """Find investors matching the given criteria."""
        query = session.query(Investor)

        # Filter by investor type
        if "investor_types" in criteria:
            types = criteria["investor_types"]
            if types:
                query = query.filter(Investor.investor_type.in_(types))

        # Filter by focus area
        if "focus_areas" in criteria:
            focus_areas = criteria["focus_areas"]
            for area in focus_areas:
                query = query.filter(Investor.focus_areas.contains([area]))

        # Filter by location
        if "location" in criteria and criteria["location"]:
            query = query.filter(Investor.location.ilike(f"%{criteria['location']}%"))

        # Pagination
        query = query.limit(100)  # Reasonable limit

        result = await session.execute(query)
        return result.scalars().all()

    async def _generate_emails_for_campaign(
        self, session: AsyncSession, campaign_id: UUID
    ):
        """Generate personalized emails for all pending targets in a campaign."""
        # Get campaign with related data
        campaign = await crud.campaign.get(session, campaign_id)
        if not campaign:
            return

        # Get template
        template = await crud.template.get(session, campaign.template_id)
        if not template:
            return

        # Get user
        user = await crud.user.get(session, campaign.user_id)
        if not user:
            return

        # Get pending targets
        targets = await crud.campaign_target.get_pending(session, campaign_id)

        for target in targets:
            # Get investor with investments and connections
            investor = await crud.investor.get(session, target.investor_id)
            if not investor:
                continue

            # Fetch investor's recent investments
            investments = await session.execute(
                select(Investment)
                .where(Investment.investor_id == investor.id)
                .order_by(Investment.investment_date.desc())
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
                )

                # Update target with generated content
                await crud.campaign_target.update(
                    session,
                    db_obj=target,
                    obj_in=CampaignTargetUpdate(
                        email_subject=subject,
                        email_body=body,
                        status="approved",  # Auto-approve for now
                    ),
                )
            except Exception as e:
                print(f"Error generating email for target {target.id}: {e}")

    async def approve_target(
        self,
        session: AsyncSession,
        target_id: UUID,
        override_notes: Optional[str] = None,
    ) -> Optional[CampaignTarget]:
        """Approve a target for sending (optionally with overrides)."""
        target = await crud.campaign_target.get(session, target_id)
        if not target:
            return None

        update_data = CampaignTargetUpdate(status="approved")
        if override_notes:
            update_data.user_override_notes = override_notes

        return await crud.campaign_target.update(
            session, db_obj=target, obj_in=update_data
        )

    async def reject_target(
        self, session: AsyncSession, target_id: UUID, reason: Optional[str] = None
    ) -> Optional[CampaignTarget]:
        """Reject a target."""
        update_data = CampaignTargetUpdate(status="rejected")
        if reason:
            update_data.user_override_notes = reason
        target = await crud.campaign_target.get(session, target_id)
        if not target:
            return None
        return await crud.campaign_target.update(
            session, db_obj=target, obj_in=update_data
        )

    async def start_campaign(
        self, session: AsyncSession, campaign_id: UUID
    ) -> Optional[Campaign]:
        """Start a campaign (change status to active)."""
        return await crud.campaign.start_campaign(session, campaign_id)

    async def get_pending_targets(
        self, session: AsyncSession, campaign_id: UUID
    ) -> List[CampaignTarget]:
        """Get all pending (approved, not sent) targets for a campaign."""
        targets = await crud.campaign_target.get_by_campaign(session, campaign_id)
        return [t for t in targets if t.status in ("approved", "pending")]

    async def mark_target_sent(
        self, session: AsyncSession, target_id: UUID, message_id: Optional[str] = None
    ) -> Optional[CampaignTarget]:
        """Mark a target as sent and create tracking record."""
        target = await crud.campaign_target.mark_sent(session, target_id)
        if target:
            # Create tracking record
            await crud.email_tracking.create(
                session, target_id=target_id, message_id=message_id
            )
        return target


# Global instance
campaign_service = CampaignService()
