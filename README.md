# PitcheRai - AI-Powered Fundraising Outreach

*Automate investor discovery and personalized outreach for startups.*

## What is PitcheRai?

PitcheRai is an autonomous agent that monitors startup funding announcements (Crunchbase, AngelList, press releases), identifies relevant VCs/angels for your specific niche, and auto-drafts personalized cold emails using recent investments, shared connections, and portfolio alignment. The agent tracks response rates, learns which templates and targets convert, and iteratively improves.

## Why Use PitcheRai?

Founders waste hours on manual outreach. PitcheRai automates the entire funnel from target discovery to first contact, while maintaining personalization that gets replies. Features:

- **Auto-discovery**: Monitors funding rounds and identifies relevant investors
- **Smart targeting**: Filters by niche, stage, portfolio overlap
- **Personalized emails**: AI-drafted using recent investments and shared connections
- **Campaign management**: Queue, schedule, track responses
- **Learning system**: Improves based on what works for your vertical
- **Dashboard**: Review targets, override drafts, view metrics

## Tech Stack

- **Backend**: Python 3.11+ with FastAPI
- **Frontend**: Streamlit dashboard
- **Database**: PostgreSQL
- **Queue**: Redis + Celery
- **APIs**: Gmail API, Crunchbase API, AngelList API, OpenRouter (LLM)
- **Testing**: pytest, ruff, pyright

## Quick Start

### Prerequisites

- Python 3.11 or 3.12
- PostgreSQL 14+
- Redis 7+
- Gmail API credentials
- Crunchbase API key
- AngelList API access
- OpenRouter API key

### Installation

1. **Clone and setup**
    ```bash
    cd pitcherai
    pip install -e .[dev]
    ```
    This uses system Python directly (no virtual environment required).

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and database credentials
   ```

3. **Initialize database**
   ```bash
   python scripts/setup_db.py
   ```

4. **Run the dashboard**
   ```bash
   python scripts/run_dashboard.py
   ```

5. **Start the worker** (in another terminal)
   ```bash
   celery -A src.campaign worker --loglevel=info
   ```

### Docker Setup (Alternative)

```bash
docker-compose up -d
```

## Usage

1. **Create a campaign**: Enter your startup details, funding stage, and industry
2. **Set your preferences**: Define investor focus areas, geographic preferences, minimum check size
3. **Let it discover**: The system monitors funding rounds and finds matching investors
4. **Review & approve**: See drafted emails in the dashboard, edit if needed, approve for sending
5. **Track results**: Monitor opens, replies, and conversions in real-time
6. **Optimize**: The system learns which templates and targets work best

## Project Structure

```
pitcherai/
├── src/                 # Source code
│   ├── collector/      # Data collection from APIs
│   ├── targeter/       # Investor filtering and ranking
│   ├── drafter/        # AI email generation
│   ├── campaign/       # Campaign orchestration
│   ├── email/          # Gmail integration
│   └── dashboard/      # Web UI
├── tests/              # Test suite
├── scripts/            # Utility scripts
├── .github/workflows/  # CI/CD pipelines
├── requirements.txt    # Dependencies
├── pyproject.toml      # Project metadata
└── ARCHITECTURE.md     # Detailed design docs
```

## Configuration

Environment variables (`.env`):

```env
DATABASE_URL=postgresql://user:password@localhost/pitcherai
REDIS_URL=redis://localhost:6379/0

# APIs
GMAIL_CLIENT_ID=your_gmail_client_id
GMAIL_CLIENT_SECRET=your_gmail_client_secret
OPENROUTER_API_KEY=your_openrouter_key
CRUNCHBASE_API_KEY=your_crunchbase_key
ANGELLIST_ACCESS_TOKEN=your_angellist_token

# App settings
SECRET_KEY=your_secret_key
DEBUG=True
```

## Testing

```bash
# Run tests with coverage
pytest tests/ -v --cov=src

# Lint
ruff check .

# Type check
pyright .
```

## CI/CD

GitHub Actions runs automated tests on every push:
- Multi-version Python testing (3.11, 3.12)
- Linting with ruff
- Type checking with pyright
- Security scanning
- Documentation validation

## Development

See `TASKS.md` for current development progress and upcoming work.

Current phase: Phase 1 - Setup & Planning

Key tasks:
- [x] Review requirements and design architecture
- [x] Set up development environment and dependencies
- [x] Create project structure
- [ ] Implement main features (Phase 2)
- [ ] Write and run tests (Phase 3)
- [ ] Documentation and deployment (Phase 4)

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed system design, data models, and API specifications.

## Contributing

Contributions welcome! Please read `CONTRIBUTING.md` (coming soon) and submit PRs.

## License

[Your License Here]

## Support

- GitHub Issues: [Create an issue](../../issues)
- Documentation: See `docs/` directory
- Email: [your-email@example.com](mailto:your-email@example.com)
