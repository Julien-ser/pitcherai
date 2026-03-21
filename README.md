# PitcheRai

**AI-Pitched** — an autonomous agent that monitors startup funding announcements (Crunchbase, AngelList, press releases), identifies relevant VCs/angels for your specific niche, and auto-drafts personalized cold emails using recent investments, shared connections, and portfolio alignment. The agent also tracks response rates, learns which templates and targets convert, and iteratively improves.

## Why

AI agents are hot, but founders still waste hours on manual outreach. This automates the funnel from target discovery to first contact, while keeping it personalized enough to actually get replies.

## Tech Stack

- **Backend**: Python 3.11/3.12
- **Database**: SQLAlchemy with SQLite (PostgreSQL supported)
- **API Integrations**: Crunchbase, AngelList, Gmail, OpenRouter
- **Task Queue**: Celery + Redis
- **Validation**: Pydantic
- **Type Checking**: Pyright
- **Linting**: Ruff
- **Testing**: Pytest

## Features

- **Funding Announcement Monitoring**: Scrape recent funding rounds from multiple sources
- **Investor Discovery**: Automatically find and rank relevant investors based on your startup profile
- **Personalized Email Drafting**: LLM-powered email generation with context from shared connections and portfolio alignment
- **Campaign Management**: Create, manage, and track outreach campaigns
- **Response Tracking**: Monitor email opens, replies, and categorize responses
- **Learning System**: Track template performance and improve conversion rates over time
- **Dashboard**: Review targets and override emails before sending

## Project Structure

```
pitcherai/
├── src/
│   ├── collector/        # Data source integrations (Crunchbase, AngelList, RSS)
│   ├── campaign/         # Celery tasks for campaign execution
│   ├── config.py         # Configuration management
│   ├── database.py       # Database engine and repositories
│   ├── drafter.py        # Email drafting with LLM
│   ├── email.py          # Gmail API integration
│   ├── models.py         # Pydantic validation models (API layer)
│   ├── models_db.py      # SQLAlchemy persistence models
│   ├── orchestrator.py   # Main application orchestrator
│   └── targeter.py       # Investor filtering and ranking
├── tests/                # Test suite
├── .github/workflows/    # CI/CD pipelines
├── README.md
└── TASKS.md              # Development task tracking
```

## Setup

### Prerequisites

- Python 3.11 or 3.12
- Redis (for Celery)
- SQLite (or PostgreSQL)

### Installation

```bash
# Clone and install
cd pitcherai
pip install uv
uv pip install -e .
```

### Configuration

Create a `.env` file:

```env
# Database
DATABASE_URL=sqlite:///./pitcherai.db

# APIs
OPENROUTER_API_KEY=your_openrouter_key
CRUNCHBASE_API_KEY=your_crunchbase_key
ANGELLIST_ACCESS_TOKEN=your_angellist_token

# Gmail
GMAIL_CLIENT_ID=your_client_id
GMAIL_CLIENT_SECRET=your_client_secret
GMAIL_REFRESH_TOKEN=your_refresh_token
EMAIL_FROM_ADDRESS=founder@yourstartup.com
EMAIL_FROM_NAME=Your Name

# Redis
REDIS_URL=redis://localhost:6379/0

# Settings
DEBUG=false
LOG_LEVEL=INFO
EMAIL_RATE_LIMIT=100
DEFAULT_MODEL=openai/gpt-4o
```

### Running

```bash
# Initialize database
python -c "from src.database import get_engine; get_engine()"

# Start Celery worker
celery -A src.campaign.celery_app worker --loglevel=info

# Run orchestrator
python -m src.orchestrator

# Start dashboard (when implemented)
# gunicorn src.dashboard:app
```

## Development

### Testing

```bash
# Run tests with coverage
pytest tests/ -v --cov=src

# Lint
ruff check .

# Type check
pyright .
```

### CI/CD

The project uses GitHub Actions with three jobs:
- **test**: Runs tests, linting, and type checks across Python 3.11 and 3.12
- **security-scan**: Checks for secrets using TruffleHog
- **documentation**: Verifies README and TASKS.md exist and are meaningful

## Current Status

**Phase 1**: Setup & Planning - In Progress
- [x] Review requirements and design architecture
- [ ] Set up development environment and dependencies
- [ ] Create project structure (core modules implemented)
- [ ] Write core unit tests
- [ ] Integrate all API clients
- [ ] Implement email drafting with LLM
- [ ] Build the dashboard interface
- [ ] Deploy and validate

## License

MIT
