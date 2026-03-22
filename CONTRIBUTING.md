# Contributing to PitcherAI

Thank you for your interest in contributing to PitcherAI! This document provides guidelines and information for contributors.

## Getting Started

### Prerequisites

- Python 3.11 or higher
- PostgreSQL database
- Redis server
- Git
- uv (Python package manager)

### Setting Up the Development Environment

1. **Fork and clone the repository:**

```bash
git clone https://github.com/your-username/pitcherai.git
cd pitcherai
```

2. **Create a virtual environment:**

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies:**

```bash
uv pip install -e ".[dev]"
```

4. **Set up environment variables:**

```bash
cp .env.example .env
# Edit .env with your local configuration
```

5. **Initialize the database:**

```bash
uv run python -c "from pitcherai.database import init_db; import asyncio; asyncio.run(init_db())"
```

6. **Run tests to ensure everything works:**

```bash
pytest tests/ -v
```

## Development Workflow

### Branching Strategy

- `main` - Stable, production-ready code
- `develop` - Integration branch for features (if applicable)
- `feature/xxx` - New features
- `bugfix/xxx` - Bug fixes
- `docs/xxx` - Documentation improvements

Always create a new branch from `main` for your changes.

### Code Style

We follow these conventions:

- **Python**: PEP 8 with Ruff linter
- **Imports**: Organized with Ruff (E, F, W, I, N, UP, etc.)
- **Type hints**: Required for all public functions
- **Docstrings**: Google style for all public functions, classes, and methods

Run linting and type checking before committing:

```bash
ruff check .
pyright .
```

### Testing

- Write unit tests for new functionality in `tests/unit/`
- Write integration tests in `tests/integration/`
- Aim for >80% code coverage
- Tests should be isolated and repeatable

Run tests:

```bash
pytest tests/ -v --cov=src --cov-report=html
```

### Commit Messages

Use clear, descriptive commit messages:

```
type: brief description

Longer description if needed.

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation changes
- style: Code style changes (formatting, etc.)
- refactor: Code refactoring
- test: Adding or updating tests
- chore: Build process, tooling, etc.
```

Example:

```
feat: Add email template A/B testing

Implement A/B testing for email templates to compare
performance metrics and learn which variants convert better.
```

### Pull Request Process

1. **Update README.md** with any new features or configuration changes
2. **Update CHANGELOG.md** with your changes
3. **Add tests** for new functionality
4. **Ensure all CI checks pass** (tests, lint, type check)
5. **Create a Pull Request** against the `main` branch
6. **Fill out the PR template** with:
   - What changes were made
   - Why they were made
   - How to test the changes
   - Any breaking changes or migration steps
   - Screenshots for UI changes

### Code Review

- All PRs require at least one review
- Address review comments promptly
- Keep PRs focused (one feature/fix per PR)
- Squash commits before merging (or use merge commits if preferred)

## Project Structure

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
├── README.md            # Main documentation
├── ARCHITECTURE.md      # System architecture
├── CONTRIBUTING.md      # This file
└── CHANGELOG.md         # Version history
```

## Key Components

### FastAPI Backend

The main API is in `src/pitcherai/main.py`. Endpoints are organized in `src/pitcherai/api/`.

### Database

Uses SQLAlchemy 2.0 with asyncpg. Database models are in `src/pitcherai/models.py`. Migrations use Alembic.

### Services

Business logic is in `src/pitcherai/services/`:

- `email_generation.py` - AI-powered email personalization
- `campaign.py` - Campaign management
- `prospecting.py` - Investor discovery and import
- `gmail.py` - Gmail API integration

### Dashboard

Streamlit dashboard in `src/pitcherai/dashboard/app.py`. Run with:

```bash
uv run streamlit run src/pitcherai/dashboard/app.py
```

### Async Tasks

Celery tasks in `src/pitcherai/tasks/` for background processing (email sending, tracking, etc.).

## Working with the Database

### Schema Changes

1. Update `src/pitcherai/models.py`
2. Create Alembic migration:
```bash
alembic revision --autogenerate -m "description"
```
3. Review the generated migration
4. Test migration locally
5. Include migration file in PR

### Querying Data

Use async session from `src/pitcherai/database.py`:

```python
from pitcherai.database import get_session
from pitcherai.crud import get_investor

async with get_session() as session:
    investor = await get_investor(session, investor_id)
```

## Environment Variables

See `.env.example` for all available configuration options. Key categories:

- Database (`DATABASE_URL`)
- Redis (`REDIS_URL`, `CELERY_BROKER_URL`)
- API settings (`API_HOST`, `API_PORT`, `SECRET_KEY`)
- OpenAI/Anthropic API keys
- External API keys (Crunchbase, AngelList, Gmail)

## Performance and Scalability

- Use async database operations
- Batch operations where possible
- Implement rate limiting for external APIs
- Use Celery for long-running tasks
- Cache frequently accessed data

## Security Considerations

- Never commit API keys or secrets
- Use environment variables for all secrets
- Validate all user inputs with Pydantic
- Implement rate limiting
- Use HTTPS in production
- Keep dependencies updated

## Troubleshooting

### Database Connection Issues

```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Test connection
uv run python -c "from pitcherai.database import test_db; import asyncio; asyncio.run(test_db())"
```

### Redis Connection Issues

```bash
# Check Redis is running
redis-cli ping
```

### Celery Worker Not Starting

```bash
# Check Redis connection
celery -A pitcherai.tasks inspect ping
```

### Import Errors

Make sure you're using uv and the virtual environment is activated:

```bash
which python  # Should point to .venv/bin/python
```

## Getting Help

- Open an issue for bug reports or feature requests
- Check existing issues before creating new ones
- Provide detailed reproduction steps for bugs
- Include logs and environment details

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Accept responsibility and apologize for mistakes
- Show empathy towards others

## License

MIT License - See LICENSE file for details (when created).

---

Thank you for contributing to PitcherAI! 🚀
