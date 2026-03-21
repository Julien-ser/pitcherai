#!/usr/bin/env python3
"""Seed database with sample data."""

import sys
from sqlalchemy import create_engine, text
from src.config import settings


def seed_database():
    """Insert sample investors and startups for testing."""
    engine = create_engine(settings.database_url)

    with engine.connect() as conn:
        # Clear existing data
        conn.execute(text("DELETE FROM outreaches;"))
        conn.execute(text("DELETE FROM campaigns;"))
        conn.execute(text("DELETE FROM investors;"))
        conn.execute(text("DELETE FROM startups;"))

        # Insert sample investors
        investors = [
            (
                "inv_001",
                "Alice Johnson",
                "alice@aivc.com",
                "AI Ventures",
                ["AI", "Machine Learning", "Computer Vision"],
                ["seed", "series-a"],
                ["DeepMind", "OpenAI"],
                ["Cohere", "Anthropic"],
                ["TechVC", "FounderFund"],
                5000000,
                50000000,
                "https://aivc.com",
            ),
            (
                "inv_002",
                "Bob Smith",
                "bob@saasfund.com",
                "SaaS Fund",
                ["SaaS", "B2B", "Enterprise"],
                ["seed", "series-a", "series-b"],
                ["Snowflake", "HubSpot"],
                ["Salesforce", "Zoom"],
                ["Bessemer", "AVP"],
                10000000,
                100000000,
                "https://saasfund.com",
            ),
            (
                "inv_003",
                "Carol Wong",
                "carol@finvc.com",
                "FinTech Capital",
                ["FinTech", "Payments", "Blockchain"],
                ["pre-seed", "seed"],
                ["Stripe", "Plaid"],
                ["Square", "Coinbase"],
                ["UnionSquare", "Andreessen"],
                2000000,
                25000000,
                "https://finvc.com",
            ),
        ]

        for inv in investors:
            conn.execute(
                text("""
                INSERT INTO investors (id, name, email, firm, focus_areas, stage_preference,
                                       portfolio, recent_investments, connections, check_size_min,
                                       check_size_max, website)
                VALUES (:id, :name, :email, :firm, :focus_areas, :stage_preference,
                        :portfolio, :recent_investments, :connections, :check_size_min,
                        :check_size_max, :website)
            """),
                {
                    "id": inv[0],
                    "name": inv[1],
                    "email": inv[2],
                    "firm": inv[3],
                    "focus_areas": inv[4],
                    "stage_preference": inv[5],
                    "portfolio": inv[6],
                    "recent_investments": inv[7],
                    "connections": inv[8],
                    "check_size_min": inv[9],
                    "check_size_max": inv[10],
                    "website": inv[11],
                },
            )

        # Insert sample startup
        conn.execute(
            text("""
            INSERT INTO startups (id, name, industry, stage, description, funding_needed, website, founders)
            VALUES ('startup_001', 'AI-Pitched', 'AI', 'seed',
                    'AI-powered fundraising outreach automation for startups', 2000000,
                    'https://pitcherai.example.com', ARRAY['Founder 1', 'Founder 2'])
        """)
        )

        conn.commit()

    print("✓ Database seeded with sample data!")
    print("  - 3 investors")
    print("  - 1 startup")


if __name__ == "__main__":
    try:
        seed_database()
        sys.exit(0)
    except Exception as e:
        print(f"✗ Error seeding database: {e}")
        sys.exit(1)
