#!/usr/bin/env python3
"""Setup database tables."""

import asyncio
import sys
from sqlalchemy import create_engine, text
from src.config import settings


def setup_database():
    """Create database tables."""
    engine = create_engine(settings.database_url)

    with engine.connect() as conn:
        # Enable pgvector if using PostgreSQL for embeddings
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))

        # Create investors table
        conn.execute(
            text("""
            CREATE TABLE IF NOT EXISTS investors (
                id VARCHAR(50) PRIMARY KEY,
                name VARCHAR(200) NOT NULL,
                email VARCHAR(200) UNIQUE NOT NULL,
                firm VARCHAR(200),
                focus_areas TEXT[],  -- array of strings
                stage_preference TEXT[],
                portfolio TEXT[],
                recent_investments TEXT[],
                connections TEXT[],
                location VARCHAR(100),
                check_size_min DECIMAL(15, 2),
                check_size_max DECIMAL(15, 2),
                website VARCHAR(200),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        )

        # Create startups table
        conn.execute(
            text("""
            CREATE TABLE IF NOT EXISTS startups (
                id VARCHAR(50) PRIMARY KEY,
                name VARCHAR(200) NOT NULL,
                industry VARCHAR(100),
                stage VARCHAR(50),
                description TEXT,
                funding_needed DECIMAL(15, 2),
                location VARCHAR(100),
                website VARCHAR(200),
                founders TEXT[],
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        )

        # Create campaigns table
        conn.execute(
            text("""
            CREATE TABLE IF NOT EXISTS campaigns (
                id VARCHAR(50) PRIMARY KEY,
                startup_id VARCHAR(50) REFERENCES startups(id),
                name VARCHAR(200) NOT NULL,
                target_criteria JSONB,
                status VARCHAR(50) DEFAULT 'draft',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                started_at TIMESTAMP,
                completed_at TIMESTAMP
            );
        """)
        )

        # Create outreaches table
        conn.execute(
            text("""
            CREATE TABLE IF NOT EXISTS outreaches (
                id VARCHAR(50) PRIMARY KEY,
                campaign_id VARCHAR(50) REFERENCES campaigns(id),
                investor_id VARCHAR(50) REFERENCES investors(id),
                template_id VARCHAR(50),
                subject TEXT NOT NULL,
                body TEXT NOT NULL,
                sent_at TIMESTAMP,
                status VARCHAR(50) DEFAULT 'draft',
                response TEXT,
                response_type VARCHAR(50),
                overridden BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        )

        # Create email_templates table
        conn.execute(
            text("""
            CREATE TABLE IF NOT EXISTS email_templates (
                id VARCHAR(50) PRIMARY KEY,
                name VARCHAR(200) NOT NULL,
                subject TEXT NOT NULL,
                body TEXT NOT NULL,
                variant VARCHAR(50),
                tone VARCHAR(50) DEFAULT 'professional',
                performance_score DECIMAL(5, 4) DEFAULT 0.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        )

        # Create indexes
        conn.execute(
            text("CREATE INDEX IF NOT EXISTS idx_investors_email ON investors(email);")
        )
        conn.execute(
            text("CREATE INDEX IF NOT EXISTS idx_investors_firm ON investors(firm);")
        )
        conn.execute(
            text(
                "CREATE INDEX IF NOT EXISTS idx_outreaches_campaign ON outreaches(campaign_id);"
            )
        )
        conn.execute(
            text(
                "CREATE INDEX IF NOT EXISTS idx_outreaches_status ON outreaches(status);"
            )
        )
        conn.execute(
            text(
                "CREATE INDEX IF NOT EXISTS idx_outreaches_sent_at ON outreaches(sent_at);"
            )
        )

        conn.commit()

    print("✓ Database tables created successfully!")
    print(f"  Using: {settings.database_url}")


if __name__ == "__main__":
    try:
        setup_database()
        sys.exit(0)
    except Exception as e:
        print(f"✗ Error setting up database: {e}")
        sys.exit(1)
