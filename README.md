# PitcherAI

**AI-Pitched** — An autonomous agent that monitors startup funding announcements, identifies relevant VCs/angels, and auto-drafts personalized cold emails. Tracks responses and learns what converts.

## Mission

Automate the fundraising outreach funnel from target discovery to first contact, while maintainingpersonalization that gets replies. Monitor Crunchbase, AngelList, and press releases to find active investors in your niche, then draft personalized emails based on their recent investments, shared connections, and portfolio alignment.

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

**Phase 1: Setup & Planning** (In Progress)
- ✅ Requirements review & architecture design
- ⏳ Set up development environment and dependencies
- ⏳ Create project structure

## Tech Stack

- Python 3.11+
- SQLite (SQLAlchemy ORM)
- Gmail API for email sending/tracking
- OpenAI API for email generation
- Streamlit for dashboard UI
- APScheduler for periodic tasks

## Quick Start (Coming Soon)

```bash
# Clone and setup
git clone <repo>
cd pitcherai
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run dashboard
python -m dashboard.app

# Or run CLI collector
python -m collector.main
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
│   ├── config.py      # Configuration management
│   └── main.py        # CLI entry point
├── tests/
├── requirements.txt
├── config/
└── ARCHITECTURE.md
```

## Development

This project uses the OpenCode agent framework for autonomous development. See `TASKS.md` for current work items.

### Running Tests

```bash
pytest tests/
```

## Environment Variables

Create a `.env` file with:

```env
OPENAI_API_KEY=your_key
GMAIL_CLIENT_ID=your_client_id
GMAIL_CLIENT_SECRET=your_secret
# ... more to be documented
```

## Roadmap

- [ ] Phase 1: Core data collection and targeting
- [ ] Phase 2: AI drafting and dashboard
- [ ] Phase 3: Email integration and tracking
- [ ] Phase 4: Learning engine and optimization
- [ ] Phase 5: Multi-user support and scaling

## Contributing

This is an autonomous project. To contribute, check the issues or modify `TASKS.md` and submit a PR.

## License

TBD
