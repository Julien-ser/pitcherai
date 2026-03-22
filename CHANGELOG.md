# Changelog

All notable changes to PitcherAI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project structure and core functionality
- FastAPI backend with RESTful endpoints
- PostgreSQL database with SQLAlchemy ORM
- Celery async task processing with Redis
- Streamlit dashboard for human-in-the-loop review
- AI-powered email generation using OpenAI GPT
- Gmail API integration for email sending
- Email tracking (opens, clicks, replies)
- Campaign management system
- Investor prospecting from Crunchbase and AngelList
- Comprehensive test suite with pytest
- GitHub Actions CI/CD pipeline
- Complete documentation (README, ARCHITECTURE, CONTRIBUTING)

### Features

- **Automated Data Collection**: Monitor funding announcements from multiple sources
- **Smart Investor Matching**: Filter investors by niche, stage, focus areas
- **AI-Powered Personalization**: Generate context-aware emails
- **Campaign Management**: Create, manage, and track outreach campaigns
- **Human Review Dashboard**: Approve/edit emails before sending
- **Response Tracking**: Monitor campaign performance metrics
- **Learning System**: Track conversion rates and improve templates

## [0.1.0] - 2026-03-21

### Added
- Initial release
- Core API endpoints for users, investors, campaigns, and templates
- Email generation service with OpenAI integration
- Gmail service with OAuth2 authentication
- Campaign service with target management
- Prospecting service with Crunchbase/AngelList integration
- Streamlit dashboard UI
- Celery tasks for async email sending and tracking
- Database models and migrations support
- Configuration management with Pydantic settings
- Environment-based configuration
- Request/response schemas with Pydantic
- Rate limiting and email frequency controls
- Database connection pooling with asyncpg
- Coverage reporting with pytest-cov
- Linting with Ruff
- Type checking with Pyright
- Complete documentation

### Documentation
- README.md with quick start guide
- ARCHITECTURE.md with system design details
- .env.example with all configuration options
- API endpoint documentation in README
- Project structure overview
- Deployment instructions for local and production

### Testing
- Unit tests for services and models
- Integration tests for API endpoints
- Database test fixtures
- Mock implementations for external APIs
- Coverage reporting setup

### CI/CD
- GitHub Actions workflow for testing
- Automated tests on push to main/develop
- Automated tests on pull requests
- Matrix testing on Python 3.11 and 3.12
- Linting and type checking in CI pipeline

[Unreleased]: https://github.com/your-username/pitcherai/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/your-username/pitcherai/releases/tag/v0.1.0
