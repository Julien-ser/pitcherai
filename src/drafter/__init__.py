"""Email Drafter - AI-powered personalized email generation"""

from datetime import datetime
import json
from typing import Dict, List, Optional
from openai import AsyncOpenAI
from ..config.config import settings
from ..database import get_db, EmailTemplate, Investor, Email


class EmailDrafter:
    """Generates personalized email drafts using AI"""

    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
        self.max_tokens = settings.openai_max_tokens
        self.temperature = settings.openai_temperature

    async def generate_email(
        self,
        investor: Investor,
        template: Optional[EmailTemplate] = None,
        context: Optional[Dict] = None,
    ) -> Dict:
        """Generate a personalized email for an investor"""

        # Build context for AI
        prompt_context = self._build_context(investor, context)

        # Get template if provided
        template_body = template.body if template else settings.default_draft_template

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {
                        "role": "user",
                        "content": self._build_user_prompt(prompt_context, template_body),
                    },
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )

            content = response.choices[0].message.content

            # Parse response into subject and body
            subject, body = self._parse_response(content, investor)

            return {"subject": subject, "body": body, "confidence": 0.85}

        except Exception as e:
            print(f"Error generating email: {e}")
            # Fallback to template
            return self._fallback_email(investor, template)

    def _build_context(self, investor: Investor, context: Optional[Dict]) -> Dict:
        """Build context dictionary for AI"""
        ctx = {
            "investor_name": investor.name,
            "investor_firm": investor.firm or "",
            "investor_title": investor.title or "",
            "recent_investment": "",
        }

        if investor.last_funding_date:
            ctx["recent_investment"] = (
                f"investment on {investor.last_funding_date.strftime('%B %Y')}"
            )

        if context:
            ctx.update(context)

        return ctx

    def _get_system_prompt(self) -> str:
        """Get system prompt for email generation"""
        return """You are an expert fundraising assistant crafting personalized cold emails to investors.

Your emails should:
- Be concise (150-200 words max)
- Reference specific, relevant details about the investor's background or investments
- Be professional but warm
- Include a clear, specific ask (e.g., "Would you be open to a 15-minute call?")
- Not be overly salesy or generic

Output format:
Subject: < compelling subject line >
< blank line >
< email body >"""

    def _build_user_prompt(self, context: Dict, template_body: str) -> str:
        """Build user prompt with context"""
        return f"""Generate a personalized cold email to {context["investor_name"]} at {context["investor_firm"]}.

Context:
{json.dumps(context, indent=2)}

Template guidance:
{template_body}

Write the email now:"""

    def _parse_response(self, content: str, investor: Investor) -> tuple:
        """Parse AI response into subject and body"""
        lines = content.strip().split("\n")
        subject = (
            f"Introduction from {settings.user_company}"
            if not settings.user_company
            else f"Investment opportunity: {settings.user_company}"
        )

        for i, line in enumerate(lines):
            if line.lower().startswith("subject:"):
                subject = line.split(":", 1)[1].strip()
                body_start = i + 2 if i + 1 < len(lines) and not lines[i + 1].strip() else i + 1
                body = "\n".join(lines[body_start:])
                break
        else:
            body = content

        return subject, body.strip()

    def _fallback_email(self, investor: Investor, template: Optional[EmailTemplate]) -> Dict:
        """Fallback email using template with simple substitution"""
        subject = f"Introduction from {settings.user_company or 'our startup'}"

        if template:
            body = template.body
        else:
            body = f"""Hi {investor.name},

I noticed your background at {investor.firm or "your firm"} and believe our startup may align with your investment thesis.

We're building something innovative and would love to share more details.

Would you be open to a brief conversation?

Best,
{settings.user_name or "Founder"}"""

        return {"subject": subject, "body": body, "confidence": 0.5}

    async def draft_for_investor(
        self, investor_id: int, template_id: Optional[int] = None
    ) -> Optional[Email]:
        """Create and save a draft email for an investor"""
        db_gen = get_db()
        db = next(db_gen)
        try:
            investor = db.query(Investor).filter_by(id=investor_id).first()
            if not investor:
                return None

            template = None
            if template_id:
                template = db.query(EmailTemplate).filter_by(id=template_id).first()

            result = self.generate_email(investor, template)

            # For async, we need to await
            if hasattr(result, "__await__"):
                result = await result

            email = Email(
                investor_id=investor_id,
                template_id=template_id,
                subject=result["subject"],
                body=result["body"],
                status="draft",
                confidence_score=result["confidence"],
                drafted_at=datetime.utcnow(),
            )

            db.add(email)
            db.commit()
            db.refresh(email)
            return email

        except Exception as e:
            print(f"Error drafting email: {e}")
            db.rollback()
            return None
        finally:
            db.close()


def create_drafter() -> EmailDrafter:
    """Factory to create EmailDrafter instance"""
    return EmailDrafter()
