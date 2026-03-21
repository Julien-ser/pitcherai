# PitcheRai - Architecture Design

## Overview
PitcheRai is an autonomous agent that automates startup fundraising outreach by monitoring funding announcements, identifying relevant investors, and drafting personalized cold emails.

## Core Components

### 1. DataCollector
Monitors funding announcements from multiple sources:
- **Crunchbase API**: Track funding rounds, company profiles, investor data
- **AngelList API**: Startup funding and investor data
- **RSS Feeds**: Press releases and news about funding announcements
- **Web Scraper**: Fallback for sources without APIs

### 2. TargetIdentifier
Filters and ranks potential investors:
- **Niche Filter**: Matches investor focus areas with startup's industry
- **Stage Matching**: Aligns with startup's funding stage (pre-seed, seed, etc.)
- **Portfolio Analysis**: Checks for competing investments in same space
- **Connection Finder**: Identifies shared connections via LinkedIn API
- **Scoring Engine**: Ranks targets by relevance and likelihood to respond

### 3. EmailDrafter
Generates personalized cold emails using LLM:
- **Template Engine**: Base templates for different investor types
- **Personalization**: Incorporates recent investments, shared connections, portfolio alignment
- **A/B Testing**: Multiple subject lines and email variants
- **Compliance**: Ensures CAN-SPAM compliance and proper opt-outs

### 4. CampaignManager
Orchestrates outreach campaigns:
- **Queue Management**: Prioritizes targets based on ranking
- **Sending Scheduler**: Respects rate limits and best send times
- **Response Tracker**: Monitors email opens, clicks, replies via Gmail API
- **Learning Engine**: Analyzes which templates/targets convert, iterates
- **Dashboard**: Web UI to review targets, override emails, view metrics

### 5. GmailIntegration
Handles email sending and response tracking:
- **OAuth2**: Secure Gmail API authentication
- **Send Queue**: Manages batch sending with throttling
- **Response Parsing**: Detects replies, categorizes interest level
- **Follow-up Scheduler**: Automated follow-ups based on response

## Data Models

```python
# Core Entities
Investor:
  - id: str
  - name: str
  - email: str
  - firm: str
  - focus_areas: List[str]
  - stage_preference: List[str]
  - portfolio: List[Company]
  - recent_investments: List[Investment]
  - connections: List[Connection]

Startup:
  - id: str
  - name: str
  - industry: str
  - stage: str
  - description: str
  - funding_needed: float

Campaign:
  - id: str
  - startup_id: str
  - targets: List[Investor]
  - templates: List[EmailTemplate]
  - status: str
  - metrics: CampaignMetrics

EmailTemplate:
  - id: str
  - subject: str
  - body: str
  - variant: str
  - performance: float

Outreach:
  - id: str
  - campaign_id: str
  - investor_id: str
  - template_id: str
  - sent_at: datetime
  - status: str
  - response: Optional[Response]
```

## Technical Stack

- **Language**: Python 3.11+
- **Web Framework**: FastAPI (dashboard API) + Streamlit or React (frontend)
- **Data Storage**: PostgreSQL (main data) + Redis (caching/queue)
- **Task Queue**: Celery + Redis for async processing
- **APIs**: Gmail API, Crunchbase API, AngelList API, LinkedIn API (optional)
- **LLM**: OpenRouter or similar for email drafting
- **Monitoring**: Prometheus + Grafana (metrics dashboard)
- **Testing**: pytest, pytest-cov, ruff (linting), pyright (type checking)

## Project Structure

```
pitcherai/
├── src/
│   ├── __init__.py
│   ├── config.py          # Configuration management
│   ├── database.py        # DB models and connections
│   ├── models.py          # Pydantic data models
│   ├── collector/
│   │   ├── __init__.py
│   │   ├── crunchbase.py
│   │   ├── angellist.py
│   │   ├── rss.py
│   │   └── scraper.py
│   ├── targeter/
│   │   ├── __init__.py
│   │   ├── filter.py
│   │   ├── ranker.py
│   │   └── connections.py
│   ├── drafter/
│   │   ├── __init__.py
│   │   ├── templates.py
│   │   ├── personalizer.py
│   │   └── llm_client.py
│   ├── campaign/
│   │   ├── __init__.py
│   │   ├── manager.py
│   │   ├── scheduler.py
│   │   └── metrics.py
│   ├── email/
│   │   ├── __init__.py
│   │   ├── gmail.py
│   │   ├── sender.py
│   │   └── tracker.py
│   └── dashboard/
│       ├── __init__.py
│       ├── api.py
│       ├── streamlit_app.py
│       └── static/
│       └── templates/
├── tests/
│   ├── __init__.py
│   ├── test_collector.py
│   ├── test_targeter.py
│   ├── test_drafter.py
│   ├── test_campaign.py
│   └── test_email.py
├── scripts/
│   ├── setup_db.py
│   ├── seed_data.py
│   └── run_dashboard.py
├── .env.example
├── .gitignore
├── pyproject.toml
├── requirements.txt
├── README.md
├── TASKS.md
└── docker-compose.yml (optional for Postgres/Redis)
```

## API Endpoints (Dashboard)

- `GET /api/investors` - List and search investors
- `GET /api/campaigns` - List campaigns
- `POST /api/campaigns` - Create new campaign
- `GET /api/campaigns/{id}` - Campaign details with metrics
- `PUT /api/outreaches/{id}` - Override draft before sending
- `POST /api/outreaches/{id}/send` - Manual send trigger
- `GET /api/metrics` - Dashboard metrics and charts

## Security Considerations

- Store all API keys in environment variables (never commit)
- Use OAuth2 for Gmail API (no passwords stored)
- Encrypt sensitive data at rest (investor emails, connections)
- Implement rate limiting on dashboard endpoints
- Validate and sanitize all user inputs
- Regular security audits with truffleHog

## Deployment Options

1. **Local Development**: Direct Python + Postgres + Redis
2. **Docker Compose**: All services containerized
3. **Cloud**: Deploy on AWS/GCP with managed databases
4. **Serverless**: Lambda functions for collectors, EC2 for dashboard

## Monitoring & Metrics

- Number of funding announcements processed daily
- Target identification accuracy rate
- Email open/response rates
- Campaign conversion rates (replies -> meetings -> investments)
- System health (API response times, queue depths)
- Cost per successful introduction

## Future Enhancements

- Multi-language email support
- Voice/video message integration
- CRM integrations (HubSpot, Salesforce)
- Advanced analytics dashboard
- Collaborative team features
- Mobile app for on-the-go approvals
