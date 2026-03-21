"""Email generation service using OpenAI."""

import os
from typing import Optional, Dict, Any
from openai import AsyncOpenAI
from ..config import settings


class EmailGenerationService:
    """Service for generating personalized emails using AI."""

    def __init__(self):
        self._client = None
        self.model = settings.openai_model

    @property
    def client(self):
        """Lazy initialization of OpenAI client."""
        if self._client is None and settings.openai_api_key:
            self._client = AsyncOpenAI(api_key=settings.openai_api_key)
        return self._client

    async def generate_email(
        self,
        investor_name: str,
        investor_firm: Optional[str],
        investor_focus: Optional[list],
        investor_recent_investments: Optional[list],
        user_startup: str,
        user_description: str,
        user_niche: str,
        template_subject: str,
        template_body: str,
        custom_vars: Optional[Dict[str, Any]] = None,
    ) -> tuple[str, str]:
        """
        Generate a personalized email for an investor.

        Args:
            investor_name: Name of the investor
            investor_firm: Firm name (if any)
            investor_focus: Focus areas/sectors
            investor_recent_investments: List of recent investments
            user_startup: Startup name
            user_description: Startup description
            user_niche: Startup's niche/industry
            template_subject: Subject template with placeholders
            template_body: Body template with placeholders
            custom_vars: Additional custom variables

        Returns:
            Tuple of (subject, body) with personalized content
        """
        # Build context for personalization
        context = self._build_context(
            investor_name=investor_name,
            investor_firm=investor_firm,
            investor_focus=investor_focus,
            investor_recent_investments=investor_recent_investments,
            user_startup=user_startup,
            user_description=user_description,
            user_niche=user_niche,
            custom_vars=custom_vars or {},
        )

        # Fill template placeholders with basic context
        subject = self._fill_template(template_subject, context)
        body_template = self._fill_template(template_body, context)

        # Use AI to enhance the personalization
        enhanced_body = await self._enhance_with_ai(
            investor_name=investor_name,
            investor_firm=investor_firm,
            investor_focus=investor_focus,
            investor_recent_investments=investor_recent_investments,
            user_startup=user_startup,
            user_description=user_description,
            user_niche=user_niche,
            base_body=body_template,
            custom_vars=custom_vars or {},
        )

        return subject, enhanced_body

    def _build_context(
        self,
        investor_name: str,
        investor_firm: Optional[str],
        investor_focus: Optional[list],
        investor_recent_investments: Optional[list],
        user_startup: str,
        user_description: str,
        user_niche: str,
        custom_vars: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Build the context dictionary for template filling."""
        context = {
            "investor_name": investor_name,
            "investor_firm": investor_firm or "",
            "investor_focus": ", ".join(investor_focus) if investor_focus else "",
            "user_startup": user_startup,
            "user_description": user_description,
            "user_niche": user_niche,
        }

        # Add personalized mention of recent investments if available
        if investor_recent_investments:
            recent = investor_recent_investments[:2]  # Top 2
            context["investor_recent_investments"] = ", ".join(
                f"{inv.get('startup_name', 'Unknown')} ({inv.get('round_type', 'round')})"
                for inv in recent
            )
        else:
            context["investor_recent_investments"] = ""

        # Merge custom vars
        context.update(custom_vars)
        return context

    def _fill_template(self, template: str, context: Dict[str, Any]) -> str:
        """Fill template placeholders with context values."""
        result = template
        for key, value in context.items():
            placeholder = f"{{{{{key}}}}}"
            result = result.replace(placeholder, str(value))
        return result

    async def _enhance_with_ai(
        self,
        investor_name: str,
        investor_firm: Optional[str],
        investor_focus: Optional[list],
        investor_recent_investments: Optional[list],
        user_startup: str,
        user_description: str,
        user_niche: str,
        base_body: str,
        custom_vars: Dict[str, Any],
    ) -> str:
        """
        Use OpenAI to enhance the email body with additional personalization.
        """
        system_prompt = """You are an expert startup fundraising copywriter. Your task is to refine cold outreach emails to make them more compelling, personalized, and effective.

Guidelines:
- Keep the email concise (150-200 words max)
- Be specific and show you've done your homework about the investor
- Mention something relevant about their portfolio or focus areas
- Clearly state what you're building and why it's interesting
- Include a clear, low-friction call to action
- Sound genuine, not generic
- Do not use overly formal language; be professional but conversational"""

        # Build investor context
        investor_context = f"Investor: {investor_name}"
        if investor_firm:
            investor_context += f" from {investor_firm}"
        if investor_focus:
            investor_context += f"\nFocus areas: {', '.join(investor_focus)}"
        if investor_recent_investments:
            investor_context += "\nRecent investments:"
            for inv in investor_recent_investments[:3]:
                investor_context += f"\n  - {inv.get('startup_name', 'Unknown')} ({inv.get('round_type', 'round')})"

        user_prompt = f"""Please refine this cold email to be more personalized and effective.

INVESTOR CONTEXT:
{investor_context}

STARTUP:
{user_startup} - {user_description}
Niche: {user_niche}

DRAFT EMAIL:
{base_body}

Make it more compelling while keeping the core message. Add specific personalization showing you understand this investor's portfolio or focus. Ensure it's concise and has a clear call to action."""

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.7,
                max_tokens=500,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            # If AI fails, return the base template as-is
            print(f"OpenAI API error: {e}")
            return base_body


# Global instance
email_generator = EmailGenerationService()
