# PitcherAI Architecture

## Overview
PitcherAI is an autonomous agent that automates VC/angel outreach for startup fundraising. It monitors funding announcements, identifies relevant investors, drafts personalized emails, tracks responses, and learns from results.

## System Components

### 1. Collector
Fetches startup funding data from multiple sources:
- **Crunchbase**: API integration for funding rounds
- **AngelList**: Scrapes/proxies investment data
- **RSS Feeds**: Press releases and news
- Output: List of recent funding events with company and investor details

### 2. Targeter
Processes collected data to identify relevant investors:
- **Filter**: Applies user-defined criteria (stage, geography, niche, check size)
- **Scorer**: Ranks investors based on portfolio alignment, recent activity, shared connections
- Output: Prioritized list of target investors with profiles

### 3. Drafter
Generates personalized email content using AI:
- **Input**: Investor profile, user's startup info, recent investments
- **Processing**: Uses OpenAI API (or similar) to create tailored drafts
- **Output**: Email drafts with subject lines, body, personalization tokens

### 4. Campaign Manager
Orchestrates the outreach workflow:
- Manages target lists and campaign settings
- Coordinates between components
- Handles scheduling and rate limiting
- Tracks campaign metrics

### 5. Email Integration
Handles email operations via Gmail API:
- **Sender**: Sends approved emails
- **Tracker**: Monitors replies, open rates (via tracking pixels or read receipts)
- **Responder**: Classifies responses (interested, not interested, out of office)

### 6. Dashboard
Web-based UI for oversight and control:
- Review and edit target lists
- Approve/modify email drafts before sending
- View campaign metrics and dashboards
- Override automated decisions
- Built with Streamlit for simplicity

### 7. Database
Persistent storage using SQLite:
- **Targets**: Investor profiles, contact info, scoring data
- **Campaigns**: Campaign definitions, settings, status
- **Emails**: Drafts, sent emails, tracking data
- **Responses**: received replies, classification
- **Metrics**: aggregated performance data for learning

### 8. Learning Engine
Analyzes performance to improve future outreach:
- Identifies which investor characteristics correlate with positive responses
- Learns which email templates perform best
- Adjusts scoring algorithms based on feedback
- A/B tests variations

## Data Flow

```
[Collector] → raw_funding_data → [Targeter] → scored_targets → [Drafter] → email_drafts
                                                                         ↓
[Dashboard] ← targets_and_drafts ← [Campaign Manager] → approved_targets → [Email] → sent_emails
                                                                                                    ↓
                                                                                               [Responses] → [Learning Engine]
                                                                                                    ↓
[Dashboard] ← updated_metrics_and_insights ← [Campaign Manager]
```

## Technology Stack

- **Language**: Python 3.11+
- **Database**: SQLite (via SQLAlchemy ORM)
- **APIs**: Gmail API, OpenAI API, optional Crunchbase/AngelList APIs
- **Web UI**: Streamlit (single-file, easy deployment)
- **Scheduling**: APScheduler or simple cron
- **Configuration**: environment variables + config file

## File Structure

```
src/
  collector/
    __init__.py
    base.py      # Base collector interface
    crunchbase.py
    angellist.py
    rss.py
  targeter/
    __init__.py
    scorer.py    # Scoring algorithms
    filter.py    # Filtering logic
  drafter/
    __init__.py
    email.py     # Email generation with AI
  campaign/
    __init__.py
    manager.py   # Campaign orchestration
    tracker.py   # Response tracking
  email/
    __init__.py
    sender.py    # Gmail API wrapper
    tracker.py   # Open/response tracking
  dashboard/
    __init__.py
    app.py      # Streamlit application
  database/
    __init__.py
    models.py   # SQLAlchemy models
    connection.py
  config.py     # Configuration loading
  main.py       # CLI entry point
tests/
  unit/
  integration/
requirements.txt
config/
  config.yaml  # Default configuration
.env.example   # Environment variable template
```

## Deployment Model

- **Development**: Local machine, SQLite file-based DB
- **Production**: VPS or cloud VM; can containerize with Docker if needed
- **Dashboard**: Streamlit Cloud or self-hosted
- **Scheduler**: Systemd cron or APScheduler embedded in dashboard process

## Key Abstractions

- **Source**: Any data source for funding/investors
- **Target**: An investor contact with metadata and score
- **Campaign**: A specific outreach effort with criteria, templates, schedule
- **Template**: Email content with placeholders for personalization
- **Metric**: Quantitative measure of campaign performance

## Extension Points

- Add new data sources by implementing Collector base class
- Customize scoring by adjusting weights or ML model
- Swap AI provider (OpenAI → Anthropic, Local LLM)
- Alternative email providers (SendGrid, Amazon SES)
- Multi-user support (currently single-founder)

## Security Considerations

- Store API keys in environment variables, never in code
- Use read-only OAuth scopes for Gmail initially
- Encrypt database if storing sensitive investor data
- Implement proper access control if multi-user

## Performance Considerations

- Respect API rate limits (Crunchbase, Gmail, OpenAI)
- Batch email sending to avoid being flagged as spam
- Implement backoff and retry logic
- Cache frequently accessed data (investor profiles)
