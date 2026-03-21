# PitcherAI

**AI-Pitched** — An autonomous agent that monitors startup funding announcements, identifies relevant VCs/angels, and auto-drafts personalized cold emails. Tracks responses and learns what converts.

## Mission

Automate the fundraising outreach funnel from target discovery to first contact, while maintaining personalization that gets replies. Monitor Crunchbase, AngelList, and press releases to find active investors in your niche, then draft personalized emails based on their recent investments, shared connections, and portfolio alignment.

## Features

- **Automated Discovery**: Continuously monitors funding announcements from multiple sources
- **Intelligent Targeting**: Scores and ranks investors based on relevance to your startup
- **Personalized Drafts**: AI-generated emails referencing recent investments and shared context
- **Dashboard Review**: Web UI to review targets and approve/modify drafts before sending
- **Response Tracking**: Monitors replies and open rates to measure performance
- **Learning Engine**: Improves targeting and templates based on what works

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed system design, component breakdown, and data flow.

## Current Status

**Phase 2: Core Implementation** (In Progress)
- ✅ Requirements review & architecture design
- ✅ Development environment and dependencies setup
- ✅ Project structure created
- ✅ Database models and ORM setup
- ✅ Collector module (funding data discovery)
- ✅ Targeter module (investor scoring & filtering)
- ✅ Drafter module (AI email generation)
- ✅ Email module (Gmail API integration)
- ✅ Campaign orchestration
- ✅ CLI interface
- ⏳ Tests and validation

## Tech Stack

- Python 3.11+
- SQLite (SQLAlchemy ORM)
- Gmail API for email sending/tracking
- OpenAI API for email generation
- Streamlit for dashboard UI
- APScheduler for periodic tasks

## Quick Start

```bash
# Clone and setup
git clone <repo>
cd pitcherai
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"

# Configure environment
cp .env.example .env
# Edit .env with your API keys:
# - OPENAI_API_KEY
# - GMAIL_CLIENT_ID, GMAIL_CLIENT_SECRET, GMAIL_REFRESH_TOKEN
# - USER_EMAIL, USER_NAME, USER_COMPANY

# Initialize database
pitcherai init

# Discover investors
pitcherai collect --limit 20

# List top investors
pitcherai list-investors --min-score 0.6

# Create a campaign
pitcherai create-campaign --name "Test Campaign"

# Launch dashboard
pitcherai dashboard
# or streamlit run src/dashboard/__init__.py
```

## Project Structure

```
pitcherai/
├── src/
│   ├── collector/     # Data collection from Crunchbase, AngelList, RSS
│   ├── targeter/      # Investor scoring and filtering
│   ├── drafter/       # AI email generation
│   ├── campaign/      # Campaign orchestration
│   ├── email/         # Gmail API integration
│   ├── dashboard/     # Streamlit UI
│   ├── database/      # Data models and persistence
│   ├── config/        # Configuration management
│   └── main.py        # CLI entry point
├── tests/
├── requirements.txt
├── pyproject.toml
├── config/
└── ARCHITECTURE.md
```

## CLI Commands

- `pitcherai init` - Initialize database tables
- `pitcherai collect` - Discover investors from funding announcements
- `pitcherai list-investors` - List investors from database
- `pitcherai create-campaign` - Create and run a full campaign
- `pitcherai send-campaign` - Send emails for a campaign
- `pitcherai dashboard` - Launch Streamlit dashboard
- `pitcherai shell` - Interactive Python shell with app context

## Development

This project uses the OpenCode agent framework for autonomous development. See `TASKS.md` for current work items.

### Running Tests

```bash
pytest tests/ -v
```

### Code Quality

```bash
ruff check src/
black src/
mypy src/
```

## Environment Variables

Create a `.env` file with:

```env
# Required
OPENAI_API_KEY=your_key

# Gmail API (OAuth 2.0)
GMAIL_CLIENT_ID=your_client_id
GMAIL_CLIENT_SECRET=your_client_secret
GMAIL_REFRESH_TOKEN=your_refresh_token
GMAIL_TOKEN_URI=https://oauth2.googleapis.com/token

# User profile
USER_EMAIL=your@email.com
USER_NAME=Your Name
USER_COMPANY=Your Company
USER_DESCRIPTION=Brief description of what your startup does

# Optional
CRUNCHBASE_API_KEY=your_key
ANGELLIST_API_KEY=your_key
DATABASE_URL=sqlite:///pitcherai.db
DEBUG=True
```

## Roadmap

- [x] Phase 1: Setup & Planning
- [x] Phase 2: Core Implementation (in progress)
- [ ] Phase 3: Testing & Integration
- [ ] Phase 4: Documentation & Deployment
- [ ] Phase 5: Learning engine & optimization
- [ ] Phase 6: Multi-user support & scaling

## Contributing

This is an autonomous project. To contribute, check the issues or modify `TASKS.md` and submit a PR.

## License

MIT

