"""PitcherAI command-line interface."""

import argparse
import asyncio
from datetime import datetime
from uuid import UUID

from pitcherai.database import init_db, close_db
from pitcherai import crud
from pitcherai.services.prospecting import prospecting_service
from pitcherai.config import settings


async def import_investors(queries: list[str], sources: list[str], limit: int):
    """Import investors from specified sources."""
    from pitcherai.database import AsyncSessionLocal

    async with AsyncSessionLocal() as db:
        count = await prospecting_service.import_investors_from_sources(
            db, queries=queries, sources=sources, limit_per_source=limit
        )
        print(f"Imported {count} investors")


async def enrich_portfolio(investor_id: str):
    """Enrich an investor's portfolio with recent investments."""
    from pitcherai.database import AsyncSessionLocal

    async with AsyncSessionLocal() as db:
        count = await prospecting_service.enrich_investor_portfolio(
            db, investor_id=UUID(investor_id)
        )
        print(f"Added {count} investments for investor {investor_id}")


async def list_campaigns(user_id: str = None):
    """List all campaigns."""
    from pitcherai.database import AsyncSessionLocal

    async with AsyncSessionLocal() as db:
        if user_id:
            campaigns = await crud.campaign.get_by_user(db, user_id=UUID(user_id))
        else:
            campaigns = await crud.campaign.get_multi(db)

        print(f"Found {len(campaigns)} campaigns:")
        for camp in campaigns:
            print(f"  {camp.name} ({camp.status}) - {camp.id}")


def main():
    """Main CLI entrypoint."""
    parser = argparse.ArgumentParser(description="PitcherAI CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Import investors command
    import_parser = subparsers.add_parser(
        "import", help="Import investors from external sources"
    )
    import_parser.add_argument(
        "--queries", nargs="+", required=True, help="Search queries"
    )
    import_parser.add_argument(
        "--sources",
        nargs="+",
        default=["crunchbase", "angellist"],
        help="Sources to import from",
    )
    import_parser.add_argument("--limit", type=int, default=50, help="Limit per source")

    # Enrich portfolio command
    enrich_parser = subparsers.add_parser("enrich", help="Enrich investor portfolio")
    enrich_parser.add_argument("investor_id", help="Investor UUID")

    # List campaigns command
    list_parser = subparsers.add_parser("list-campaigns", help="List campaigns")
    list_parser.add_argument("--user-id", help="Filter by user UUID")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Initialize database
    asyncio.run(init_db())

    try:
        if args.command == "import":
            asyncio.run(import_investors(args.queries, args.sources, args.limit))
        elif args.command == "enrich":
            asyncio.run(enrich_portfolio(args.investor_id))
        elif args.command == "list-campaigns":
            asyncio.run(list_campaigns(args.user_id))
    finally:
        asyncio.run(close_db())


if __name__ == "__main__":
    main()
