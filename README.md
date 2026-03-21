# PitcherAI

**AI-Powered Autonomous VC Outreach Agent**

An autonomous agent that monitors startup funding announcements, identifies relevant VCs and angel investors for your specific niche, and auto-drafts personalized cold emails using recent investments, shared connections, and portfolio alignment. The agent tracks response rates, learns which templates and targets convert, and iteratively improves.

## Features

- **Automated Data Collection**: Monitor Crunchbase, AngelList, and press releases for funding announcements
- **Smart Investor Matching**: Identify investors based on niche, stage preferences, focus areas, and portfolio alignment
- **AI-Powered Personalization**: Generate highly personalized emails using OpenAI GPT or Anthropic Claude
- **Campaign Management**: Create and manage outreach campaigns with target lists
- **Human-in-the-Loop Review**: Dashboard to review, edit, and approve emails before sending
- **Gmail Integration**: Send emails via Gmail API with rate limiting and tracking
- **Response Tracking**: Monitor opens, clicks, and replies to measure effectiveness
- **Learning System**: Track performance and learn which templates/targets convert best

## Tech Stack

- **Backend**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL with asyncpg
- **Async Tasks**: Celery + Redis
- **Dashboard**: Streamlit
- **AI**: OpenAI GPT / Anthropic Claude
- **Email**: Gmail API
- **Testing**: pytest, pytest-cov
- **Linting**: Ruff
- **Type Checking**: Pyright
- **CI/CD**: GitHub Actions

## Project Status

**Phase 2**: Core Implementation - In Progress

- [x] Review requirements and design architecture
- [x] Set up development environment and dependencies
- [x] Create project structure
- [x] Implement database models and schemas ✅
- [x] Build core API endpoints ✅
- [x] Implement AI email generation ✅
- [x] Build Streamlit dashboard ✅
- [x] Implement CLI tool ✅
- [ ] Write and run tests
- [ ] Deploy and validate

See [TASKS.md](TASKS.md) for full task list.

## Quick Start

### Prerequisites

- Python 3.11 or higher
- PostgreSQL database
- Redis server (for Celery)
- API keys for:
  - OpenAI (or Anthropic Claude)
  - Gmail API (OAuth2 credentials)

### Installation

1. Clone the repository:
```bash
cd pitcherai
```

2. Install dependencies using uv:
```bash
pip install uv
uv pip install -e .
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys and database settings
```

4. Initialize the database:
```bash
uv run python -c "from pitcherai.database import init_db; import asyncio; asyncio.run(init_db())"
```

5. Run the FastAPI server:
```bash
uv run python -m pitcherai.main
```

The API will be available at http://localhost:8000

6. (Optional) Run the Streamlit dashboard:
```bash
uv run streamlit run src/pitcherai/dashboard/app.py
```

## Configuration

Create a `.env` file in the project root with the following variables:

```ini
# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/pitcherai

# Redis
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2

# API Settings
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=false
SECRET_KEY=your-secret-key-here

# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini

# Gmail API (Optional)
GMAIL_CLIENT_ID=...
GMAIL_CLIENT_SECRET=...
GMAIL_REFRESH_TOKEN=...
DEFAULT_FROM_EMAIL=your-app@gmail.com

# Email Sending Limits
MAX_EMAILS_PER_DAY=50
EMAIL_FREQUENCY=1
```

See `.env.example` for all available options.

## API Endpoints

### Users
- `POST /api/users` - Create user
- `GET /api/users/{id}` - Get user
- `PUT /api/users/{id}` - Update user

### Investors
- `GET /api/investors` - List investors (with filters)
- `POST /api/investors` - Bulk create investors
- `GET /api/investors/{id}` - Get investor details
- `GET /api/investors/{id}/investments` - Get portfolio

### Campaigns
- `POST /api/campaigns` - Create campaign
- `GET /api/campaigns` - List campaigns
- `GET /api/campaigns/{id}` - Get campaign
- `PUT /api/campaigns/{id}` - Update campaign
- `POST /api/campaigns/{id}/start` - Start campaign
- `POST /api/campaigns/{id}/pause` - Pause campaign
- `GET /api/campaigns/{id}/targets` - Get campaign targets

### Email Generation
- `POST /api/generate-email` - Generate personalized email
- `POST /api/generate-campaign-emails` - Generate emails for campaign

### Templates
- `GET /api/templates` - List templates
- `POST /api/templates` - Create template
- `PUT /api/templates/{id}` - Update template

### Analytics
- `GET /api/analytics/campaign/{campaign_id}` - Campaign metrics
- `GET /api/analytics/dashboard` - Overall metrics

## Dashboard

The Streamlit dashboard provides a user-friendly interface for:
- Reviewing and editing generated emails before sending
- Approving/rejecting targets
- Monitoring campaign performance
- Viewing response rates and analytics

## Database Schema

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed database schema and system architecture.

## Development

### Running Tests

```bash
pytest tests/ -v --cov=src --cov-report=html
```

### Linting and Type Checking

```bash
ruff check .
pyright .
```

### Project Structure

```
.
├── src/pitcherai/
│   ├── __init__.py
│   ├── main.py           # FastAPI application
│   ├── config.py         # Configuration management
│   ├── database.py       # Database connection
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic schemas
│   ├── crud.py           # CRUD operations
│   ├── api/              # API routers
│   ├── services/         # Business logic
│   ├── tasks/            # Celery tasks
│   ├── dashboard/        # Streamlit dashboard
│   └── utils/            # Utilities
├── tests/
│   ├── unit/
│   └── integration/
├── data/                 # Data files (CSV, JSON)
├── logs/                 # Application logs
├── pyproject.toml       # Project dependencies
├── .env.example         # Environment template
└── ARCHITECTURE.md      # System architecture
```

## CI/CD

GitHub Actions workflows are configured in `.github/workflows/`:

- `test.yml` - Runs tests, linting, type checks
- `deploy-staging.yml` - Deploy to staging
- `deploy-production.yml` - Deploy to production

## License

MIT
