# PitcherAI Application
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml uv.lock* ./

# Install uv and dependencies
RUN pip install --no-cache-dir uv && \
    uv pip install --system --no-cache-dir -e .

# Copy application code
COPY src/ /app/src/

# Create necessary directories
RUN mkdir -p /app/data /app/logs

# Expose ports
EXPOSE 8000 8501

# Run migrations and start application
CMD ["sh", "-c", "uv run python -c \"from pitcherai.database import init_db; import asyncio; asyncio.run(init_db())\" && uvicorn pitcherai.main:app --host 0.0.0.0 --port 8000"]
