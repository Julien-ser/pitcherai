# PitcherAI System Architecture

## Overview

PitcherAI is an AI-powered autonomous VC outreach agent that automates the entire process of finding investors, personalizing cold emails, and tracking campaign performance.

## System Components

### 1. FastAPI Backend (`src/pitcherai/main.py`)

RESTful API with the following main endpoints:

- **Users**: `/api/users` - Manage startup user profiles
- **Investors**: `/api/investors` - CRUD for investor profiles
- **Templates**: `/api/templates` - Email template management
- **Campaigns**: `/api/campaigns` - Campaign creation and management
- **Campaign Targets**: `/api/campaigns/{id}/targets` - Manage campaign targets
- **Email Generation**: `/api/generate-email` - AI-powered email personalization
- **Prospecting**: `/api/prospecting/import` - Import investors from external sources
- **Analytics**: `/api/analytics/*` - Campaign performance metrics
- **Tracking**: `/api/tracking/*` - Email open and reply tracking

### 2. Database Schema

PostgreSQL database with the following tables:

- **users**: Startup profiles (email, name, description, niche)
- **investors**: VC/angel profiles with focus areas, location, etc.
- **investments**: Track investor's portfolio companies and rounds
- **shared_connections**: Mutual connections between user and investors
- **templates**: Email templates with subject/body placeholders
- **campaigns**: Outreach campaigns with criteria
- **campaign_targets**: Individual investor targets for campaigns
- **email_tracking**: Track opens, clicks, and replies
- **analytics**: Daily campaign performance snapshots

### 3. Services

#### Email Generation Service (`services/email_generation.py`)
Uses OpenAI GPT-4 to personalize email templates based on:
- Investor's recent investments
- Focus areas and portfolio
- User's startup description
- Template structure

#### Campaign Service (`services/campaign.py`)
Manages campaign lifecycle:
- Creating campaigns with target criteria
- Finding matching investors
- Generating emails for targets
- Approving/rejecting targets
- Starting/pausing campaigns

#### Prospecting Service (`services/prospecting.py`)
Discovers and imports investors from:
- Crunchbase API
- AngelList API
Enriches investor profiles with portfolio data.

#### Gmail Service (`services/gmail.py`)
Handles email delivery via Gmail API with rate limiting and tracking.

### 4. Celery Tasks (`tasks/__init__.py`)

Asynchronous background jobs:
- `send_single_email`: Send individual emails with tracking
- `generate_and_send_campaign_emails`: Batch email generation and sending
- `track_email_opens`: Process open tracking pixels
- `track_email_replies`: Process reply webhooks

### 5. Streamlit Dashboard (`dashboard/app.py`)

Web-based UI for:
- Reviewing generated emails before sending
- Approving/rejecting campaign targets
- Monitoring campaign performance
- Viewing analytics and metrics

### 6. CLI (`cli.py`)

Command-line interface for:
- Importing investors from external sources
- Enriching investor portfolios
- Managing campaigns

## Data Flow

### Campaign Creation Flow

1. User creates campaign with target criteria (e.g., focus areas, investor types)
2. System queries database for matching investors
3. Creates campaign target records
4. Generates personalized emails for each target
5. Emails await human review (or auto-approve)
6. Approved targets are queued for sending via Celery
7. Emails are sent through Gmail API with rate limiting
8. Opens and replies are tracked

### Email Generation Flow

1. Fetch investor profile and recent investments
2. Retrieve user's startup profile
3. Load email template
4. Fill template placeholders with basic data
5. Enhance with AI for personalization
6. Store generated content in campaign_target
7. Display for review in dashboard

### Prospecting Flow

1. Provide search queries (e.g., "AI", "SaaS", "FinTech")
2. Query Crunchbase/AngelList APIs
3. Parse and normalize investor data
4. Check for duplicates
5. Import new investors to database
6. Optionally enrich with portfolio investments

## Configuration

All configuration via environment variables (see `.env.example`):
- Database and Redis connections
- API keys (OpenAI, Gmail, Crunchbase, AngelList)
- Email sending limits
- Celery broker settings

## Deployment

### Local Development

1. Install dependencies: `uv pip install -e .`
2. Set up `.env` file from `.env.example`
3. Initialize database: `python -c "from pitcherai.database import init_db; import asyncio; asyncio.run(init_db())"`
4. Start FastAPI: `uv run python -m pitcherai.main`
5. Start Celery worker: `celery -A pitcherai.tasks worker --loglevel=info`
6. Start Streamlit dashboard: `uv run streamlit run src/pitcherai/dashboard/app.py`

### Production

- Use PostgreSQL and Redis managed services
- Run FastAPI with gunicorn/uvicorn
- Run Celery with appropriate concurrency
- Set up GitHub Actions CI/CD
- Configure proper security (HTTPS, firewall, secrets)

## API Design Principles

- RESTful endpoints with JSON payloads
- UUID for all resource identifiers
- Consistent error responses (HTTP status codes)
- Async SQLAlchemy for database operations
- Pydantic schemas for request/response validation

## Scaling Considerations

- Database connection pooling (pool_size=10, max_overflow=20)
- Celery for asynchronous task processing
- Rate limiting on email sending (configurable)
- Caching strategies for frequently accessed data
- Pagination for list endpoints
