# PitcherAI Architecture Design

## System Overview

PitcherAI is an autonomous agent that automates VC/angel investor outreach by:
- Monitoring startup funding announcements
- Identifying relevant investors based on niche
- Auto-drafting personalized cold emails
- Tracking responses and learning from results

## Architecture Components

### 1. Data Collection Layer
- **Crunchbase Scraper**: API integration or scraping for funding data
- **AngelList Scraper**: Monitor startup investments
- **Press Monitor**: RSS feeds and news APIs for funding announcements
- **Optional**: LinkedIn API for shared connections

### 2. Data Processing Layer
- **Investor Profile Builder**: Normalize and enrich investor data
- **Niche Matching Engine**: Match investor focus areas to user's startup niche
- **Portfolio Analyzer**: Analyze investment patterns and portfolio alignment

### 3. AI/Personalization Layer
- **Email Generator**: LLM-based email drafting (OpenAI GPT, Anthropic Claude)
- **Personalization Context Builder**: Gather data for personalization hooks
- **Template Manager**: A/B test different email templates

### 4. Campaign Management Layer
- **Target List Manager**: Curate and prioritize target investors
- **Campaign Scheduler**: Plan and sequence outreach
- **Override/Dashboard**: Human review and manual send control
- **Email Sender**: Gmail API integration with rate limiting

### 5. Tracking & Learning Layer
- **Response Tracker**: Monitor opens, clicks, replies
- **Analytics Engine**: Calculate response rates and conversion metrics
- **Learning System**: Optimize templates and targeting based on performance

### 6. Presentation Layer
- **Dashboard (Streamlit)**: Review targets, approve/reject emails, view metrics
- **REST API (FastAPI)**: Backend service for all operations

## Technology Stack

- **Backend**: Python 3.11+
- **API**: FastAPI
- **Database**: PostgreSQL
- **Async Tasks**: Celery + Redis
- **Dashboard**: Streamlit
- **AI**: OpenAI API / Anthropic Claude
- **Email**: Gmail API
- **Package Manager**: uv
- **Testing**: pytest, pytest-cov
- **Linting**: Ruff
- **Type Checking**: Pyright
- **CI/CD**: GitHub Actions

## Database Schema

```sql
-- Users/startups
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    startup_name VARCHAR(255) NOT NULL,
    startup_description TEXT,
    niche VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- VC firms and investors
CREATE TABLE investors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL, -- 'vc', 'angel', 'fund'
    firm_name VARCHAR(255),
    email VARCHAR(255),
    linkedin_url TEXT,
    focus_areas JSONB, -- array of investment sectors
    stage_preferences JSONB, -- 'seed', 'series_a', etc.
    location VARCHAR(255),
    source VARCHAR(100), -- 'crunchbase', 'angellist', etc.
    raw_data JSONB, -- original data from source
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Startup investments (for portfolio analysis)
CREATE TABLE investments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    investor_id UUID REFERENCES investors(id),
    startup_name VARCHAR(255) NOT NULL,
    investment_date DATE,
    round_type VARCHAR(100),
    amount_usd DECIMAL(15,2),
    source VARCHAR(100),
    raw_data JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Shared connections (if LinkedIn integration)
CREATE TABLE shared_connections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    investor_id UUID REFERENCES investors(id),
    connection_name VARCHAR(255),
    connection_email VARCHAR(255),
    relationship VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Email templates
CREATE TABLE templates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    subject_template TEXT NOT NULL,
    body_template TEXT NOT NULL,
    variant_id VARCHAR(100), -- for A/B testing
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Campaigns
CREATE TABLE campaigns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    name VARCHAR(255) NOT NULL,
    status VARCHAR(50) DEFAULT 'draft', -- 'draft', 'active', 'paused', 'completed'
    template_id UUID REFERENCES templates(id),
    target_criteria JSONB, -- filter criteria for targets
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Target investors for a campaign
CREATE TABLE campaign_targets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    campaign_id UUID REFERENCES campaigns(id),
    investor_id UUID REFERENCES investors(id),
    status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'approved', 'rejected', 'sent'
    email_subject TEXT,
    email_body TEXT,
    scheduled_send_at TIMESTAMP,
    sent_at TIMESTAMP,
    user_override_notes TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Email tracking
CREATE TABLE email_tracking (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    campaign_target_id UUID REFERENCES campaign_targets(id),
    message_id VARCHAR(255), -- Gmail message ID
    opens_count INT DEFAULT 0,
    clicks_count INT DEFAULT 0,
    replied_at TIMESTAMP,
    bounced_at TIMESTAMP,
    last_opened_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Analytics
CREATE TABLE analytics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    campaign_id UUID REFERENCES campaigns(id),
    date DATE NOT NULL,
    sent_count INT DEFAULT 0,
    open_count INT DEFAULT 0,
    click_count INT DEFAULT 0,
    reply_count INT DEFAULT 0,
    open_rate DECIMAL(5,2),
    reply_rate DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(campaign_id, date)
);
```

## API Design (FastAPI)

### Core Endpoints

**Users**
- `POST /api/users` - Create user
- `GET /api/users/{id}` - Get user profile
- `PUT /api/users/{id}` - Update user profile

**Investors**
- `GET /api/investors` - List investors (with filters)
- `POST /api/investors` - Bulk create investors (admin)
- `GET /api/investors/{id}` - Get investor details
- `GET /api/investors/{id}/investments` - Get investor's portfolio

**Campaigns**
- `POST /api/campaigns` - Create campaign
- `GET /api/campaigns` - List campaigns
- `GET /api/campaigns/{id}` - Get campaign details
- `PUT /api/campaigns/{id}` - Update campaign
- `DELETE /api/campaigns/{id}` - Delete campaign
- `POST /api/campaigns/{id}/start` - Start campaign
- `POST /api/campaigns/{id}/pause` - Pause campaign

**Campaign Targets**
- `GET /api/campaigns/{id}/targets` - Get campaign targets with status
- `POST /api/campaigns/{id}/targets` - Add targets to campaign
- `PUT /api/campaigns/{id}/targets/{target_id}` - Update target (override email, approve/reject)
- `POST /api/campaigns/{id}/targets/{target_id}/send` - Manually send to specific target

**Templates**
- `GET /api/templates` - List templates
- `POST /api/templates` - Create template
- `GET /api/templates/{id}` - Get template
- `PUT /api/templates/{id}` - Update template

**Email Generation**
- `POST /api/generate-email` - Generate personalized email for investor
- `POST /api/generate-campaign-emails` - Generate emails for all targets in campaign

**Analytics**
- `GET /api/analytics/campaign/{campaign_id}` - Get campaign analytics
- `GET /api/analytics/dashboard` - Get overall dashboard metrics

**Dashboard (Streamlit)**
- Separate Streamlit app that calls the same FastAPI backend

## Data Flow

1. **Data Ingestion** (daily cron)
   - Fetch new funding announcements from Crunchbase/AngelList
   - Extract investor information and create/update investor records
   - Fetch related investment data for portfolio analysis

2. **Target Identification**
   - User defines their startup profile (niche, stage, location)
   - System matches investors based on:
     - Focus area alignment
     - Stage preference match
     - Recent investment activity
     - Portfolio overlap
     - Location (if relevant)

3. **Campaign Creation**
   - User selects targets and email template
   - System generates personalized emails for each target using LLM
   - Emails are created as "pending" campaign targets

4. **Human Review** (Dashboard)
   - User reviews generated emails in Streamlit dashboard
   - User can approve, reject, or edit emails before sending
   - User can schedule send times

5. **Email Sending**
   - Approved emails are sent via Gmail API
   - Rate limiting applied to avoid spam flags
   - Tracking pixels and click tracking enabled

6. **Response Tracking**
   - Monitor replies via Gmail API
   - Track opens (pixel) and clicks (tracked links)
   - Update analytics daily

7. **Learning Loop**
   - Calculate performance metrics (open rate, reply rate)
   - Identify high-performing templates and target segments
   - Suggest optimizations for future campaigns

## Security Considerations

- Store all API keys in environment variables / secret management
- Use OAuth2 for API authentication (JWT)
- Encrypt sensitive data at rest
- Implement rate limiting on API
- Follow email best practices to avoid spam (SPF, DKIM, warm-up)
- GDPR compliance: data retention, right to delete

## Scalability

- Use database connection pooling
- Cache frequently accessed data in Redis
- Process data ingestion asynchronously with Celery
- Queue email sending to manage rate limits
- Implement pagination on all list endpoints
- Consider read replicas for dashboard queries

## Deployment

- Deploy backend on cloud (Fly.io, Railway, Render, or AWS)
- Deploy database on managed service (Supabase, RDS, Neon)
- Deploy Streamlit on Streamlit Cloud or as separate service
- Use GitHub Actions for CI/CD (already configured)
- Environment-based configuration (dev/staging/prod)

## Initial Implementation Order

Phase 1 (Setup & Planning) - Current Task:
- [x] Design architecture (this document)
- [ ] Create pyproject.toml with dependencies
- [ ] Create src/ directory structure
- [ ] Set up database schema
- [ ] Create .env.example

Phase 2 (Core Implementation):
- [ ] Set up FastAPI boilerplate
- [ ] Create database models (SQLAlchemy)
- [ ] Implement basic CRUD for investors, campaigns
- [ ] Implement email generation with OpenAI
- [ ] Implement Gmail API sender
- [ ] Build Streamlit dashboard

Phase 3 & 4: Testing, Documentation, Deployment
