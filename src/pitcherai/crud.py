"""CRUD operations for all models."""

from sqlalchemy import select, and_, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List, Any
from uuid import UUID
from datetime import datetime, date, timezone

from .models import (
    User,
    Investor,
    Investment,
    SharedConnection,
    Template,
    Campaign,
    CampaignTarget,
    EmailTracking,
    Analytics,
)
from .schemas import (
    UserCreate,
    UserUpdate,
    InvestorCreate,
    InvestorUpdate,
    TemplateCreate,
    TemplateUpdate,
    CampaignCreate,
    CampaignUpdate,
    CampaignTargetCreate,
    CampaignTargetUpdate,
)


# User CRUD
class UserCRUD:
    def __init__(self):
        self.model = User

    async def get(self, session: AsyncSession, id: UUID) -> Optional[User]:
        result = await session.execute(select(User).where(User.id == id))
        return result.scalar_one_or_none()

    async def get_by_email(self, session: AsyncSession, email: str) -> Optional[User]:
        result = await session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create(self, session: AsyncSession, obj_in: UserCreate) -> User:
        obj_data = obj_in.model_dump()
        db_obj = User(**obj_data)
        session.add(db_obj)
        await session.flush()
        await session.refresh(db_obj)
        return db_obj

    async def update(
        self, session: AsyncSession, db_obj: User, obj_in: UserUpdate
    ) -> User:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        await session.flush()
        await session.refresh(db_obj)
        return db_obj

    async def delete(self, session: AsyncSession, id: UUID) -> bool:
        result = await session.execute(delete(User).where(User.id == id))
        return result.rowcount > 0

    async def get_multi(
        self, session: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[User]:
        result = await session.execute(select(User).offset(skip).limit(limit))
        return result.scalars().all()


# Investor CRUD
class InvestorCRUD:
    def __init__(self):
        self.model = Investor

    async def get(self, session: AsyncSession, id: UUID) -> Optional[Investor]:
        from sqlalchemy.orm import selectinload

        result = await session.execute(
            select(Investor)
            .where(Investor.id == id)
            .options(selectinload(Investor.investments))
        )
        return result.scalar_one_or_none()

    async def get_by_email(
        self, session: AsyncSession, email: str
    ) -> Optional[Investor]:
        result = await session.execute(select(Investor).where(Investor.email == email))
        return result.scalar_one_or_none()

    async def create(self, session: AsyncSession, obj_in: InvestorCreate) -> Investor:
        obj_data = obj_in.model_dump()
        db_obj = Investor(**obj_data)
        session.add(db_obj)
        await session.flush()
        await session.refresh(db_obj)
        return db_obj

    async def update(
        self, session: AsyncSession, db_obj: Investor, obj_in: InvestorUpdate
    ) -> Investor:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        await session.flush()
        await session.refresh(db_obj)
        return db_obj

    async def delete(self, session: AsyncSession, id: UUID) -> bool:
        result = await session.execute(delete(Investor).where(Investor.id == id))
        return result.rowcount > 0

    async def get_multi(
        self, session: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[Investor]:
        result = await session.execute(select(Investor).offset(skip).limit(limit))
        return result.scalars().all()

    async def list_by_type(
        self, session: AsyncSession, investor_type: str, skip: int = 0, limit: int = 100
    ) -> List[Investor]:
        result = await session.execute(
            select(Investor)
            .where(Investor.investor_type == investor_type)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def search_by_focus(
        self, session: AsyncSession, focus_area: str, skip: int = 0, limit: int = 100
    ) -> List[Investor]:
        # Fetch all investors and filter in Python for SQLite compatibility
        result = await session.execute(select(Investor))
        investors = result.scalars().all()
        filtered = [
            inv
            for inv in investors
            if inv.focus_areas and focus_area in inv.focus_areas
        ]
        # Apply pagination
        start = max(skip, 0)
        end = start + limit if limit is not None else None
        return filtered[start:end]


# Template CRUD
class TemplateCRUD:
    def __init__(self):
        self.model = Template

    async def get(self, session: AsyncSession, id: UUID) -> Optional[Template]:
        result = await session.execute(select(Template).where(Template.id == id))
        return result.scalar_one_or_none()

    async def create(self, session: AsyncSession, obj_in: TemplateCreate) -> Template:
        obj_data = obj_in.model_dump()
        db_obj = Template(**obj_data)
        session.add(db_obj)
        await session.flush()
        await session.refresh(db_obj)
        return db_obj

    async def update(
        self, session: AsyncSession, db_obj: Template, obj_in: TemplateUpdate
    ) -> Template:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        await session.flush()
        await session.refresh(db_obj)
        return db_obj

    async def delete(self, session: AsyncSession, id: UUID) -> bool:
        result = await session.execute(delete(Template).where(Template.id == id))
        return result.rowcount > 0

    async def get_multi(
        self, session: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[Template]:
        result = await session.execute(select(Template).offset(skip).limit(limit))
        return result.scalars().all()

    async def get_active(self, session: AsyncSession) -> List[Template]:
        result = await session.execute(
            select(Template).where(Template.is_active == True)
        )
        return result.scalars().all()


# Campaign CRUD
class CampaignCRUD:
    def __init__(self):
        self.model = Campaign

    async def get(self, session: AsyncSession, id: UUID) -> Optional[Campaign]:
        result = await session.execute(select(Campaign).where(Campaign.id == id))
        return result.scalar_one_or_none()

    async def create(self, session: AsyncSession, obj_in: CampaignCreate) -> Campaign:
        obj_data = obj_in.model_dump()
        db_obj = Campaign(**obj_data)
        session.add(db_obj)
        await session.flush()
        await session.refresh(db_obj)
        return db_obj

    async def update(
        self, session: AsyncSession, db_obj: Campaign, obj_in: CampaignUpdate
    ) -> Campaign:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        await session.flush()
        await session.refresh(db_obj)
        return db_obj

    async def delete(self, session: AsyncSession, id: UUID) -> bool:
        result = await session.execute(delete(Campaign).where(Campaign.id == id))
        return result.rowcount > 0

    async def get_multi(
        self, session: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[Campaign]:
        result = await session.execute(select(Campaign).offset(skip).limit(limit))
        return result.scalars().all()

    async def get_by_user(
        self, session: AsyncSession, user_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[Campaign]:
        result = await session.execute(
            select(Campaign)
            .where(Campaign.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def start_campaign(
        self, session: AsyncSession, campaign_id: UUID
    ) -> Optional[Campaign]:
        update_data = CampaignUpdate(
            status="active", started_at=datetime.now(timezone.utc)
        )
        return await self.update(
            session, db_obj=await self.get(session, campaign_id), obj_in=update_data
        )

    async def complete_campaign(
        self, session: AsyncSession, campaign_id: UUID
    ) -> Optional[Campaign]:
        update_data = CampaignUpdate(
            status="completed", completed_at=datetime.now(timezone.utc)
        )
        return await self.update(
            session, db_obj=await self.get(session, campaign_id), obj_in=update_data
        )


# CampaignTarget CRUD
class CampaignTargetCRUD:
    def __init__(self):
        self.model = CampaignTarget

    async def get(self, session: AsyncSession, id: UUID) -> Optional[CampaignTarget]:
        result = await session.execute(
            select(CampaignTarget).where(CampaignTarget.id == id)
        )
        return result.scalar_one_or_none()

    async def create(
        self, session: AsyncSession, obj_in: CampaignTargetCreate
    ) -> CampaignTarget:
        obj_data = obj_in.model_dump()
        db_obj = CampaignTarget(**obj_data)
        session.add(db_obj)
        await session.flush()
        await session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        session: AsyncSession,
        db_obj: CampaignTarget,
        obj_in: CampaignTargetUpdate,
    ) -> CampaignTarget:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        await session.flush()
        await session.refresh(db_obj)
        return db_obj

    async def delete(self, session: AsyncSession, id: UUID) -> bool:
        result = await session.execute(
            delete(CampaignTarget).where(CampaignTarget.id == id)
        )
        return result.rowcount > 0

    async def get_multi(
        self, session: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[CampaignTarget]:
        result = await session.execute(select(CampaignTarget).offset(skip).limit(limit))
        return result.scalars().all()

    async def get_by_campaign(
        self, session: AsyncSession, campaign_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[CampaignTarget]:
        result = await session.execute(
            select(CampaignTarget)
            .where(CampaignTarget.campaign_id == campaign_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_pending(
        self, session: AsyncSession, campaign_id: UUID
    ) -> List[CampaignTarget]:
        result = await session.execute(
            select(CampaignTarget).where(
                and_(
                    CampaignTarget.campaign_id == campaign_id,
                    CampaignTarget.status == "pending",
                )
            )
        )
        return result.scalars().all()

    async def mark_sent(
        self, session: AsyncSession, target_id: UUID
    ) -> Optional[CampaignTarget]:
        update_data = CampaignTargetUpdate(
            status="sent", sent_at=datetime.now(timezone.utc)
        )
        return await self.update(
            session, db_obj=await self.get(session, target_id), obj_in=update_data
        )


# EmailTracking CRUD
class EmailTrackingCRUD:
    def __init__(self):
        self.model = EmailTracking

    async def get(self, session: AsyncSession, id: UUID) -> Optional[EmailTracking]:
        result = await session.execute(
            select(EmailTracking).where(EmailTracking.id == id)
        )
        return result.scalar_one_or_none()

    async def get_by_target(
        self, session: AsyncSession, target_id: UUID
    ) -> Optional[EmailTracking]:
        result = await session.execute(
            select(EmailTracking).where(EmailTracking.campaign_target_id == target_id)
        )
        return result.scalar_one_or_none()

    async def create(
        self, session: AsyncSession, target_id: UUID, message_id: Optional[str] = None
    ) -> EmailTracking:
        db_obj = EmailTracking(campaign_target_id=target_id, message_id=message_id)
        session.add(db_obj)
        await session.flush()
        await session.refresh(db_obj)
        return db_obj

    async def update_open(
        self, session: AsyncSession, target_id: UUID
    ) -> Optional[EmailTracking]:
        tracking = await self.get_by_target(session, target_id)
        if tracking:
            tracking.opens_count += 1
            tracking.last_opened_at = datetime.now(timezone.utc)
            await session.flush()
            await session.refresh(tracking)
        return tracking

    async def update_reply(
        self, session: AsyncSession, target_id: UUID
    ) -> Optional[EmailTracking]:
        tracking = await self.get_by_target(session, target_id)
        if tracking:
            tracking.replied_at = datetime.now(timezone.utc)
            await session.flush()
            await session.refresh(tracking)
        return tracking


# Analytics CRUD
class AnalyticsCRUD:
    def __init__(self):
        self.model = Analytics

    async def get(self, session: AsyncSession, id: UUID) -> Optional[Analytics]:
        result = await session.execute(select(Analytics).where(Analytics.id == id))
        return result.scalar_one_or_none()

    async def get_by_campaign_date(
        self, session: AsyncSession, campaign_id: UUID, date_val: date
    ) -> Optional[Analytics]:
        result = await session.execute(
            select(Analytics).where(
                and_(Analytics.campaign_id == campaign_id, Analytics.date == date_val)
            )
        )
        return result.scalar_one_or_none()

    async def create_or_update(
        self,
        session: AsyncSession,
        campaign_id: UUID,
        date_val: date,
        sent_count: int = 0,
        open_count: int = 0,
        click_count: int = 0,
        reply_count: int = 0,
    ) -> Analytics:
        analytics = await self.get_by_campaign_date(session, campaign_id, date_val)
        if analytics:
            analytics.sent_count = sent_count
            analytics.open_count = open_count
            analytics.click_count = click_count
            analytics.reply_count = reply_count
            if sent_count > 0:
                analytics.open_rate = (open_count / sent_count) * 100
                analytics.reply_rate = (reply_count / sent_count) * 100
            await session.flush()
            await session.refresh(analytics)
        else:
            open_rate = (sent_count > 0) and (open_count / sent_count) * 100 or None
            reply_rate = (sent_count > 0) and (reply_count / sent_count) * 100 or None
            analytics = Analytics(
                campaign_id=campaign_id,
                date=date_val,
                sent_count=sent_count,
                open_count=open_count,
                click_count=click_count,
                reply_count=reply_count,
                open_rate=open_rate,
                reply_rate=reply_rate,
            )
            session.add(analytics)
            await session.flush()
            await session.refresh(analytics)
        return analytics


from sqlalchemy import delete

# Instantiate CRUD objects
user = UserCRUD()
investor = InvestorCRUD()
template = TemplateCRUD()
campaign = CampaignCRUD()
campaign_target = CampaignTargetCRUD()
email_tracking = EmailTrackingCRUD()
analytics = AnalyticsCRUD()
