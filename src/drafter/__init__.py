"""AI-powered email drafting module."""

import logging
from typing import Any, List
import httpx
from src.models import EmailTemplate, Investor, Startup

logger = logging.getLogger(__name__)

# Default templates for different variants
DEFAULT_TEMPLATES = {
    "cold_pitch": {
        "subject": "{startup_name} - {industry} Innovation",
        "body": """Dear {investor_name},

I hope this email finds you well. I'm reaching out because I noticed your strong focus on {industry} at {firm}.

{personalization_points}

We're {startup_name}, a {stage} startup building {description}. We're raising ${funding_needed:,.0f} to scale our solution.

Given your expertise in {industry}, I believe our mission aligns with your investment thesis. Would you be open to a brief conversation about our progress and vision?

Best regards,
{founder_name}
{founder_email}""",
    },
    "warm_intro": {
        "subject": "Mutual Connection: {connection_name} | {startup_name}",
        "body": """Dear {investor_name},

Our mutual connection {connection_name} suggested I reach out to you.

{personalization_points}

I'm {founder_name}, founder of {startup_name}, a {stage} startup in the {industry} space. {description}

We're currently raising ${funding_needed:,.0f} and given your focus on {industry}, I thought you'd be interested in learning more.

Would you be available for a quick call next week?

Best,
{founder_name}
{founder_email}""",
    },
    "followup": {
        "subject": "Following up: {startup_name}",
        "body": """Hi {investor_name},

I wanted to follow up on my previous email about {startup_name}.

We've made exciting progress: {recent_achievement}

Still seeking ${funding_needed:,.0f} to accelerate growth.

Would love to connect if you're still evaluating opportunities in {industry}.

{founder_name}
{founder_email}""",
    },
}


class TemplateEngine:
    """Email template management."""

    def __init__(self):
        self.templates: List[EmailTemplate] = []
        self._load_default_templates()

    def _load_default_templates(self):
        """Load default templates."""
        for variant, data in DEFAULT_TEMPLATES.items():
            template = EmailTemplate(
                id=f"tpl_{variant}",
                name=f"{variant.replace('_', ' ').title()} Template",
                subject=data["subject"],
                body=data["body"],
                variant=variant,
                tone="professional",
            )
            self.templates.append(template)

    def get_template_by_variant(self, variant: str) -> EmailTemplate | None:
        """Get a template by variant type."""
        for template in self.templates:
            if template.variant == variant:
                return template
        # Return first template as fallback
        return self.templates[0] if self.templates else None

    def render_template(
        self, template: EmailTemplate, context: dict[str, Any]
    ) -> tuple[str, str]:
        """Render template with given context."""
        try:
            # Render subject and body separately
            subject = template.subject.format(**context)
            body = template.body.format(**context)
            return subject, body
        except KeyError as e:
            logger.error(f"Missing context key for template: {e}")
            return template.subject, template.body


class Personalizer:
    """Personalize email content based on investor and startup."""

    def __init__(self, llm_client=None):
        self.llm_client = llm_client

    def extract_recent_investments(self, investor: Investor) -> List[str]:
        """Extract recent investments for personalization."""
        return investor.recent_investments[-3:] if investor.recent_investments else []

    def extract_common_connections(
        self, founder_email: str, investor: Investor
    ) -> List[str]:
        """Identify shared connections."""
        return investor.connections or []

    def generate_personalization_points(
        self, startup: Startup, investor: Investor
    ) -> List[str]:
        """Generate bullet points for email personalization."""
        points = []
        if investor.recent_investments:
            investments = ", ".join(investor.recent_investments[:2])
            points.append(f"Noted your recent investment in {investments}")
        if investor.connections:
            points.append(
                f"We have a mutual connection: {', '.join(investor.connections[:2])}"
            )
        if startup.industry.lower() in [area.lower() for area in investor.focus_areas]:
            points.append(f"Your focus on {startup.industry} aligns with our mission")
        return points

    async def draft_email(
        self,
        startup: Startup,
        investor: Investor,
        template_variant: str,
        founder_name: str = "",
        founder_email: str = "",
    ) -> EmailTemplate:
        """Draft a personalized email."""
        template_engine = TemplateEngine()
        template = template_engine.get_template_by_variant(template_variant)

        if not template:
            raise ValueError(f"Template variant {template_variant} not found")

        # Build context for rendering
        personalization_points = self.generate_personalization_points(startup, investor)
        personalization_text = (
            "\n".join([f"- {p}" for p in personalization_points])
            if personalization_points
            else ""
        )

        context = {
            "startup_name": startup.name,
            "industry": startup.industry,
            "stage": startup.stage,
            "description": startup.description,
            "funding_needed": startup.funding_needed,
            "investor_name": investor.name,
            "firm": investor.firm,
            "founder_name": founder_name,
            "founder_email": founder_email,
            "personalization_points": personalization_text,
            "connection_name": investor.connections[0] if investor.connections else "",
        }

        subject, body = template_engine.render_template(template, context)

        # Update template with rendered content
        return EmailTemplate(
            id=template.id,
            name=template.name,
            subject=subject,
            body=body,
            variant=template.variant,
            tone=template.tone,
            performance_score=0.0,
        )

        context = {
            "startup_name": startup.name,
            "industry": startup.industry,
            "stage": startup.stage,
            "description": startup.description,
            "funding_needed": startup.funding_needed,
            "investor_name": investor.name,
            "firm": investor.firm,
            "founder_name": founder_name,
            "founder_email": founder_email,
            "personalization_points": personalization_text,
            "connection_name": investor.connections[0] if investor.connections else "",
        }

        subject, body = template_engine.render_template(template, context)

        # Update template with rendered content
        return EmailTemplate(
            id=template.id,
            name=template.name,
            subject=subject,
            body=body,
            variant=template.variant,
            tone=template.tone,
        )


class LLMClient:
    """Client for LLM API (OpenRouter)."""

    def __init__(self, api_key: str, model: str = "anthropic/claude-3.5-sonnet"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://openrouter.ai/api/v1"

    async def generate_email(self, prompt: str, max_tokens: int = 1000) -> str:
        """Generate email content via LLM."""
        if not self.api_key:
            logger.warning("No OpenRouter API key provided, using fallback generation")
            return "Please configure OPENROUTER_API_KEY for AI-generated emails."

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        data = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert email writer for startup fundraising outreach.",
                },
                {"role": "user", "content": prompt},
            ],
            "max_tokens": max_tokens,
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=30.0,
                )
                response.raise_for_status()
                result = response.json()
                return result["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"LLM API call failed: {e}")
            return f"AI generation failed: {str(e)}"

    def build_prompt(
        self, startup: Startup, investor: Investor, personalization: List[str]
    ) -> str:
        """Build a prompt for email generation."""
        prompt = f"""Write a professional cold email from {startup.name} to {investor.name} at {investor.firm}.

STARTUP:
- Name: {startup.name}
- Industry: {startup.industry}
- Stage: {startup.stage}
- Description: {startup.description}
- Funding Needed: ${startup.funding_needed:,.0f}

INVESTOR:
- Name: {investor.name}
- Firm: {investor.firm}
- Focus Areas: {", ".join(investor.focus_areas)}
- Stage Preference: {", ".join(investor.stage_preference)}
- Recent Investments: {", ".join(investor.recent_investments[:3]) if investor.recent_investments else "None listed"}
- Connections: {", ".join(investor.connections) if investor.connections else "None"}

PERSONALIZATION POINTS:
{chr(10).join(f"- {p}" for p in personalization) if personalization else "- None specific, use general pitch"}

Write a concise, professional email (subject + body) that:
1. Has an attention-grabbing but professional subject line
2. Shows you've done research on the investor
3. Briefly explains what the startup does
4. States the funding round clearly
5. Has a clear call to action (request a meeting/call)
6. Is no more than 3-4 paragraphs

Return in this format:
Subject: [subject line]

[email body]"""

        return prompt
