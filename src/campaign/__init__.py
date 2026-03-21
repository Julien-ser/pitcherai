"""Campaign module - orchestrates outreach campaigns"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional
from ..database import (
    get_db,
    Campaign,
    Investor,
    Email,
    CampaignInvestor,
    InvestorStatus,
    EmailStatus,
)
from .targeter import create_targeter
from .drafter import create_drafter
from .email import create_email_sender
from ..config.config import settings


class CampaignOrchestrator:
    """Manages outreach campaigns from discovery to sending"""

    def __init__(self):
        self.targeter = create_targeter()
        self.drafter = create_drafter()
        self.sender = create_email_sender()

    def create_campaign(
        self, name: str, description: str = "", target_criteria: Dict = None
    ) -> Campaign:
        """Create a new campaign"""
        db = get_db()
        try:
            campaign = Campaign(
                name=name,
                description=description,
                target_criteria=str(target_criteria) if target_criteria else "{}",
            )
            db.add(campaign)
            db.commit()
            db.refresh(campaign)
            return campaign
        except Exception as e:
            print(f"Error creating campaign: {e}")
            db.rollback()
            raise
        finally:
            db.close()

    def add_investors_to_campaign(self, campaign_id: int, investor_ids: List[int]) -> int:
        """Add investors to a campaign"""
        db = get_db()
        try:
            campaign = db.query(Campaign).filter_by(id=campaign_id).first()
            if not campaign:
                return 0

            added = 0
            for inv_id in investor_ids:
                # Check if already added
                existing = (
                    db.query(CampaignInvestor)
                    .filter_by(campaign_id=campaign_id, investor_id=inv_id)
                    .first()
                )
                if not existing:
                    link = CampaignInvestor(campaign_id=campaign_id, investor_id=inv_id)
                    db.add(link)
                    added += 1

            campaign.total_investors = (
                campaign.investors.count() if hasattr(campaign, "investors") else added
            )
            db.commit()
            return added
        except Exception as e:
            print(f"Error adding investors: {e}")
            db.rollback()
            return 0
        finally:
            db.close()

    def generate_drafts_for_campaign(
        self, campaign_id: int, template_id: Optional[int] = None
    ) -> int:
        """Generate email drafts for all investors in a campaign"""
        db = get_db()
        try:
            # Get campaign investors without drafts
            links = (
                db.query(CampaignInvestor).filter_by(campaign_id=campaign_id, status="draft").all()
            )

            drafted = 0
            for link in links:
                # Check if email already exists
                existing = (
                    db.query(Email)
                    .filter_by(investor_id=link.investor_id, campaign_id=campaign_id)
                    .first()
                )

                if not existing:
                    email = self.drafter.draft_for_investor(
                        investor_id=link.investor_id, template_id=template_id
                    )
                    if email:
                        link.email_id = email.id
                        drafted += 1

            db.commit()
            return drafted
        except Exception as e:
            print(f"Error generating drafts: {e}")
            db.rollback()
            return 0
        finally:
            db.close()

    def send_campaign_emails(self, campaign_id: int, batch_size: int = 10) -> Dict:
        """Send emails for a campaign"""
        db = get_db()
        try:
            # Get draft emails for campaign
            query = (
                db.query(Email)
                .join(CampaignInvestor)
                .filter(CampaignInvestor.campaign_id == campaign_id, Email.status == "draft")
                .limit(batch_size)
            )

            emails = query.all()
            email_ids = [e.id for e in emails]

            results = self.sender.send_batch(email_ids)

            sent_count = sum(1 for success in results.values() if success)
            return {"total": len(emails), "sent": sent_count, "failed": len(emails) - sent_count}
        except Exception as e:
            print(f"Error sending campaign emails: {e}")
            return {"total": 0, "sent": 0, "failed": 0}
        finally:
            db.close()

    def run_full_campaign(
        self, name: str, raw_investors: List[Dict], target_criteria: Dict = None
    ) -> Dict:
        """Run a complete campaign from discovery to drafting"""
        try:
            # Create campaign
            campaign = self.create_campaign(name, target_criteria=target_criteria)

            # Score and add investors
            scored = self.targeter.discover_and_score(raw_investors)
            investor_ids = [item["investor"].id for item in scored]
            self.add_investors_to_campaign(campaign.id, investor_ids)

            # Generate drafts
            drafts = self.generate_drafts_for_campaign(campaign.id)

            return {
                "campaign_id": campaign.id,
                "investors_added": len(investor_ids),
                "drafts_generated": drafts,
                "status": "created",
            }
        except Exception as e:
            print(f"Error running campaign: {e}")
            return {"error": str(e)}


def create_campaign_orchestrator() -> CampaignOrchestrator:
    """Factory for CampaignOrchestrator"""
    return CampaignOrchestrator()
