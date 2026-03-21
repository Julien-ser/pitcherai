"""PitcherAI - Main CLI entry point"""

import click
from datetime import datetime
from .config.config import settings
from .database import init_db, get_db
from .collector import discoverer as collector_discoverer
from .targeter import create_targeter
from .campaign import create_campaign_orchestrator
from .drafter import create_drafter
from .email import create_email_sender
from .database.models import Investor, InvestorStatus


@click.group()
def cli():
    """PitcherAI CLI - AI-powered VC outreach automation"""
    pass


@cli.command()
def init():
    """Initialize database"""
    click.echo("Initializing database...")
    init_db()
    click.echo("✓ Database initialized")


@cli.command()
@click.option("--limit", default=50, help="Number of investors to discover")
def collect(limit: int):
    """Discover investors from funding announcements"""
    click.echo(f"Discovering investors (limit: {limit})...")
    # Run async discovery
    import asyncio

    announcements = asyncio.run(collector_discoverer.discover_all())
    raw_investors = collector_discoverer.extract_investors(announcements)

    # Score and save
    targeter = create_targeter()
    scored = targeter.discover_and_score(raw_investors[:limit])

    click.echo(f"✓ Discovered and saved {len(scored)} investors")


@cli.command()
@click.option("--min-score", default=0.5, help="Minimum relevance score")
def list_investors(min_score: float):
    """List investors from database"""
    db = get_db()
    try:
        investors = (
            db.query(Investor)
            .filter(Investor.relevance_score >= min_score)
            .order_by(Investor.relevance_score.desc())
            .limit(20)
            .all()
        )

        click.echo("Top Investors:")
        click.echo("-" * 80)
        for inv in investors:
            click.echo(f"{inv.name:30} {inv.firm or 'N/A':20} Score: {inv.relevance_score:.2f}")
    finally:
        db.close()


@cli.command()
@click.option("--name", required=True, help="Campaign name")
@click.option("--min-score", default=0.6, help="Minimum score for investors")
def create_campaign(name: str, min_score: float):
    """Create and run a full campaign"""
    click.echo(f"Creating campaign: {name}")

    # Discover investors (recent)
    import asyncio

    announcements = asyncio.run(collector_discoverer.discover_all())
    raw_investors = collector_discoverer.extract_investors(announcements)

    # Run campaign
    orchestrator = create_campaign_orchestrator()
    result = orchestrator.run_full_campaign(
        name=name, raw_investors=raw_investors, target_criteria={"min_score": min_score}
    )

    click.echo(f"✓ Campaign created (ID: {result.get('campaign_id')})")
    click.echo(f"  Investors added: {result.get('investors_added')}")
    click.echo(f"  Drafts generated: {result.get('drafts_generated')}")


@cli.command()
@click.option("--campaign-id", type=int, required=True, help="Campaign ID")
@click.option("--batch-size", default=10, help="Number of emails to send")
def send_campaign(campaign_id: int, batch_size: int):
    """Send emails for a campaign"""
    click.echo(f"Sending campaign {campaign_id} (batch size: {batch_size})...")

    orchestrator = create_campaign_orchestrator()
    result = orchestrator.send_campaign_emails(campaign_id, batch_size)

    click.echo(f"✓ Sent: {result['sent']}, Failed: {result['failed']}")


@cli.command()
def dashboard():
    """Launch Streamlit dashboard"""
    click.echo("Starting PitcherAI dashboard...")
    import subprocess
    import sys

    subprocess.run([sys.executable, "-m", "streamlit", "run", "src/dashboard/__init__.py"])


@cli.command()
def shell():
    """Open Python shell with app context"""
    click.echo("Starting interactive shell...")
    from .config.config import settings
    from .database import init_db, get_db, engine
    from .collector import discoverer
    from .targeter import create_targeter
    from .drafter import create_drafter
    from .campaign import create_campaign_orchestrator

    click.echo(
        "Available variables: settings, engine, db, discoverer, targeter, drafter, orchestrator"
    )
    init_db()
    db = next(get_db())

    # Enter interactive mode
    import code

    code.interact(local=globals())


if __name__ == "__main__":
    cli()
