# Deployment Guide

This guide covers deploying PitcherAI to various environments using Docker.

## Prerequisites

- Docker 20.10+ and Docker Compose 2.0+
- PostgreSQL 15+ and Redis 7+ (if deploying without Docker)
- API keys for OpenAI and Gmail API (optional)

## Quick Start (Local with Docker)

The fastest way to get started is with Docker Compose:

1. Clone the repository and navigate to the project directory:
```bash
cd pitcherai
```

2. Create a `.env` file from the production template:
```bash
cp .env.production .env
# Edit .env and add your API keys
```

3. Start all services:
```bash
docker-compose up -d
```

4. Initialize the database:
```bash
docker-compose exec web uv run python -c "from pitcherai.database import init_db; import asyncio; asyncio.run(init_db())"
```

5. Access the services:
   - API Documentation: http://localhost:8000/docs
   - API Endpoints: http://localhost:8000
   - Streamlit Dashboard: http://localhost:8501

## Manual Deployment (Without Docker)

If you prefer to deploy on your own infrastructure:

### 1. Server Requirements

- Ubuntu 20.04+ or similar Linux distribution
- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Nginx (for reverse proxy)
- systemd (for process management)

### 2. Setup Steps

```bash
# Install Python dependencies
pip install uv
uv pip install -e .

# Configure environment
cp .env.production .env
# Edit .env with your production values

# Initialize database
uv run python -c "from pitcherai.database import init_db; import asyncio; asyncio.run(init_db())"

# Copy systemd service files (see below)
sudo cp deploy/ pitcherai-web.service /etc/systemd/system/
sudo cp deploy/ pitcherai-celery-worker.service /etc/systemd/system/
sudo cp deploy/ pitcherai-celery-beat.service /etc/systemd/system/

# Reload systemd and start services
sudo systemctl daemon-reload
sudo systemctl enable pitcherai-web pitcherai-celery-worker pitcherai-celery-beat
sudo systemctl start pitcherai-web pitcherai-celery-worker pitcherai-celery-beat

# Setup Nginx configuration
sudo cp deploy/nginx-pitcherai.conf /etc/nginx/sites-available/pitcherai
sudo ln -s /etc/nginx/sites-available/pitcherai /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 3. Systemd Service Files

See the `deploy/` directory for complete systemd service configurations.

## Cloud Deployments

### Heroku

```bash
heroku create pitcherai
heroku addons:create heroku-postgresql:15
heroku addons:create heroku-redis:7

# Set config vars
heroku config:set OPENAI_API_KEY=sk-... SECRET_KEY=... etc.

# Deploy
git push heroku main
```

### Railway

```bash
railway init
# Add PostgreSQL and Redis plugins
# Set environment variables in railway.app
railway up
```

### Fly.io

```bash
fly launch --now
fly secrets set OPENAI_API_KEY=sk-... SECRET_KEY=...
fly postgres attach --database-name pitcherai
fly redis attach
fly deploy
```

## Database Migrations

When making changes to models:

1. Generate migration:
```bash
uv run alembic revision --autogenerate -m "Description"
```

2. Apply migration:
```bash
uv run alembic upgrade head
```

With Docker Compose:
```bash
docker-compose exec web uv run alembic upgrade head
```

## Monitoring

### Health Checks

- API Health: `GET /health`
- Celery Worker: `docker-compose logs celery-worker`

### Logs

```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f web
docker-compose logs -f celery-worker
docker-compose logs -f dashboard
```

## Production Checklist

- [ ] Set strong, unique `SECRET_KEY`
- [ ] Use strong PostgreSQL password
- [ ] Enable HTTPS with SSL certificates
- [ ] Configure firewall rules (only expose 80/443)
- [ ] Set up automated backups for PostgreSQL
- [ ] Configure monitoring and alerting
- [ ] Set up log aggregation
- [ ] Review and adjust Celery worker concurrency
- [ ] Configure rate limiting for Gmail API
- [ ] Set up error tracking (Sentry, etc.)

## Troubleshooting

### Database Connection Issues

Ensure PostgreSQL is running and credentials are correct:
```bash
docker-compose logs postgres
docker-compose exec web python -c "from pitcherai.database import engine; print(engine.connect())"
```

### Celery Worker Not Starting

Check Redis connection and task imports:
```bash
docker-compose logs celery-worker
docker-compose exec web uv run python -c "from pitcherai.tasks import *"
```

### Dashboard Cannot Connect to API

Verify API_BASE_URL is set correctly in dashboard environment:
```bash
docker-compose exec dashboard env | grep API_BASE_URL
```

## Maintenance

### Updating

```bash
docker-compose pull
docker-compose up -d
```

### Backups

```bash
# PostgreSQL backup
docker-compose exec postgres pg_dump -U pitcherai pitcherai > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore
cat backup_*.sql | docker-compose exec -T postgres psql -U pitcherai pitcherai
```

## Support

For deployment issues, please check [CONTRIBUTING.md](CONTRIBUTING.md) or open an issue on GitHub.
