"""Data collection module for funding announcements."""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Any, List, Optional, Dict
import re
import feedparser

from src.models import Investor, Startup

logger = logging.getLogger(__name__)


class CrunchbaseCollector:
    """Collect funding data from Crunchbase API."""

    def __init__(self, api_key: str = None):
        self.api_key = api_key
        # Mock data for demo when API key not provided
        self.mock_investors = [
            {
                "id": "inv_cb_001",
                "name": "Alice Johnson",
                "email": "alice@aiventures.com",
                "firm": "AI Ventures",
                "focus_areas": ["AI", "Machine Learning", "LLMs"],
                "stage_preference": ["seed", "series-a"],
                "portfolio": ["DataFlow AI", "NeuralBot", "ChatEngine"],
                "recent_investments": ["2025-03-01: DataFlow AI - Series A - $15M"],
                "connections": ["John Smith (ex-Google)"],
                "location": "San Francisco, CA",
                "check_size_min": 500000,
                "check_size_max": 5000000,
                "website": "https://aiventures.com",
            },
            {
                "id": "inv_cb_002",
                "name": "Bob Martinez",
                "email": "bob@saasfund.com",
                "firm": "SaaS Fund",
                "focus_areas": ["SaaS", "B2B", "Productivity"],
                "stage_preference": ["series-a", "series-b"],
                "portfolio": ["TaskMaster", "CloudSync"],
                "recent_investments": ["2025-02-15: TaskMaster - Series B - $30M"],
                "connections": [],
                "location": "New York, NY",
                "check_size_min": 2000000,
                "check_size_max": 20000000,
                "website": "https://saasfund.com",
            },
        ]

    async def fetch_recent_fundings(self, days_back: int = 7) -> List[Dict[str, Any]]:
        """Fetch funding announcements from last N days."""
        logger.info(f"Fetching funding rounds from Crunchbase (last {days_back} days)")

        if not self.api_key:
            # Return mock data
            logger.info("Using mock Crunchbase data (no API key)")
            await asyncio.sleep(0.1)  # Simulate async I/O
            cutoff = datetime.now() - timedelta(days=days_back)
            mock_rounds = [
                {
                    "id": "round_001",
                    "company_name": "TechFlow Inc",
                    "industry": "AI",
                    "stage": "seed",
                    "amount": 2500000,
                    "date": (datetime.now() - timedelta(days=3)).isoformat(),
                    "investor_ids": ["inv_cb_001"],
                },
                {
                    "id": "round_002",
                    "company_name": "CloudSync Pro",
                    "industry": "SaaS",
                    "stage": "series-a",
                    "amount": 8000000,
                    "date": (datetime.now() - timedelta(days=5)).isoformat(),
                    "investor_ids": ["inv_cb_002"],
                },
            ]
            return mock_rounds

        # TODO: Implement real async API call to Crunchbase
        logger.warning("Real Crunchbase API integration not yet implemented")
        await asyncio.sleep(0.1)
        return []

    async def get_investor_details(self, investor_id: str) -> Optional[Investor]:
        """Get detailed investor information."""
        logger.info(f"Fetching investor details: {investor_id}")

        if not self.api_key:
            # Return mock data if investor_id matches
            await asyncio.sleep(0.1)
            for inv_data in self.mock_investors:
                if inv_data["id"] == investor_id:
                    return Investor(**inv_data)
            return None

        # TODO: Implement real async API call
        logger.warning("Real Crunchbase API integration not yet implemented")
        await asyncio.sleep(0.1)
        return None


class AngelListCollector:
    """Collect funding data from AngelList."""

    def __init__(self, access_token: str = None):
        self.access_token = access_token
        self.mock_startups = [
            {
                "id": "startup_al_001",
                "name": "InnovateTech",
                "industry": "AI",
                "stage": "seed",
                "description": "AI-powered workflow automation platform",
                "funding_needed": 1500000,
                "location": "Austin, TX",
                "website": "https://innovatetech.com",
                "founders": ["Sarah Connor", "John Reese"],
            },
            {
                "id": "startup_al_002",
                "name": "CloudBase",
                "industry": "SaaS",
                "stage": "series-a",
                "description": "Enterprise cloud management solution",
                "funding_needed": 5000000,
                "location": "Denver, CO",
                "website": "https://cloudbase.io",
                "founders": ["Mike Ross"],
            },
        ]
        self.mock_investors = [
            Investor(
                id="inv_al_001",
                name="Sarah Kim",
                email="sarah@futurefund.com",
                firm="Future Fund",
                focus_areas=["AI", "ML", "Deep Tech"],
                stage_preference=["seed", "pre-seed"],
                portfolio=["InnovateTech", "DataLabs"],
                recent_investments=["2025-03-01: DataLabs - Seed - $2M"],
                connections=[],
                location="San Francisco, CA",
                check_size_min=250000,
                check_size_max=3000000,
                website="https://futurefund.com",
            ),
            Investor(
                id="inv_al_002",
                name="David Chen",
                email="david@scalevc.com",
                firm="Scale VC",
                focus_areas=["SaaS", "Enterprise", "B2B"],
                stage_preference=["series-a", "series-b"],
                portfolio=["CloudBase", "EnterpriseX"],
                recent_investments=["2025-02-20: EnterpriseX - Series A - $12M"],
                connections=["Reed Hastings"],
                location="New York, NY",
                check_size_min=3000000,
                check_size_max=15000000,
                website="https://scalevc.com",
            ),
        ]

    async def fetch_startups(self) -> List[Dict[str, Any]]:
        """Fetch startups that recently raised funding."""
        logger.info("Fetching startups from AngelList")

        if not self.access_token:
            logger.info("Using mock AngelList data (no access token)")
            await asyncio.sleep(0.1)
            return self.mock_startups

        # TODO: Implement real async API call
        logger.warning("Real AngelList API integration not yet implemented")
        await asyncio.sleep(0.1)
        return []

    async def fetch_funding_announcements(self) -> List[Dict[str, Any]]:
        """Fetch funding announcements from AngelList."""
        logger.info("Fetching funding announcements from AngelList")

        if not self.access_token:
            logger.info("Using mock AngelList data (no access token)")
            await asyncio.sleep(0.1)
            mock_announcements = [
                {
                    "id": "ann_001",
                    "company_id": "startup_al_001",
                    "company_name": "InnovateTech",
                    "industry": "AI",
                    "stage": "seed",
                    "amount": 1500000,
                    "date": (datetime.now() - timedelta(days=2)).isoformat(),
                    "investor_ids": ["inv_al_001"],
                },
                {
                    "id": "ann_002",
                    "company_name": "CloudBase",
                    "industry": "SaaS",
                    "stage": "series-a",
                    "amount": 5000000,
                    "date": (datetime.now() - timedelta(days=6)).isoformat(),
                    "investor_ids": ["inv_al_002"],
                },
            ]
            return mock_announcements

        # TODO: Implement real async API call
        logger.warning("Real AngelList API integration not yet implemented")
        await asyncio.sleep(0.1)
        return []

    async def search_investors(self, criteria: Dict[str, Any]) -> List[Investor]:
        """Search for investors by criteria."""
        logger.info(f"Searching investors with criteria: {criteria}")

        if not self.access_token:
            await asyncio.sleep(0.1)
            # Simple filtering on mock investors
            filtered = []
            for inv in self.mock_investors:
                match = True
                if "industry" in criteria:
                    if criteria["industry"].lower() not in [
                        area.lower() for area in inv.focus_areas
                    ]:
                        match = False
                if "stage" in criteria:
                    if criteria["stage"] not in inv.stage_preference:
                        match = False
                if match:
                    filtered.append(inv)
            return filtered

        # TODO: Implement real async API call
        logger.warning("Real AngelList API integration not yet implemented")
        await asyncio.sleep(0.1)
        return []


class RSSFeedCollector:
    """Monitor RSS feeds for funding news."""

    def __init__(self, feed_urls: List[str] = None):
        self.feed_urls = feed_urls or [
            "https://techcrunch.com/feed/",
            "https://feeds.feedburner.com/venturebeat/tech",
        ]

    async def parse_feeds(self, days_back: int = 7) -> List[Dict[str, Any]]:
        """Parse all configured RSS feeds for funding announcements."""
        logger.info(f"Parsing {len(self.feed_urls)} RSS feeds for funding news")
        # Run feedparser in a thread pool since it's blocking
        loop = asyncio.get_event_loop()
        announcements = await loop.run_in_executor(
            None, self._parse_feeds_sync, days_back
        )
        logger.info(f"Found {len(announcements)} funding announcements from RSS")
        return announcements

    def _parse_feeds_sync(self, days_back: int) -> List[Dict[str, Any]]:
        """Synchronous feed parsing."""
        announcements = []
        cutoff_date = datetime.now() - timedelta(days=days_back)

        for url in self.feed_urls:
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries:
                    # Parse publication date
                    published = None
                    if hasattr(entry, "published_parsed") and entry.published_parsed:
                        published = datetime(*entry.published_parsed[:6])
                    elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
                        published = datetime(*entry.updated_parsed[:6])

                    if published and published < cutoff_date:
                        continue  # Too old

                    title = entry.get("title", "").lower()
                    summary = entry.get("summary", "").lower()
                    content = title + " " + summary

                    # Detect funding announcements
                    funding_keywords = [
                        "funding",
                        "raises",
                        "raised",
                        "investment",
                        "venture capital",
                        "series",
                        "seed round",
                    ]
                    if any(keyword in content for keyword in funding_keywords):
                        announcement = {
                            "id": f"rss_{hash(entry.get('link', ''))}",
                            "title": entry.get("title", ""),
                            "link": entry.get("link", ""),
                            "published": published.isoformat() if published else None,
                            "summary": entry.get("summary", ""),
                            "source": feed.feed.get("title", "Unknown"),
                            "company_name": self._extract_company_name(
                                entry.get("title", "")
                            ),
                            "amount": self._extract_amount(entry.get("summary", "")),
                        }
                        announcements.append(announcement)

            except Exception as e:
                logger.error(f"Failed to parse RSS feed {url}: {e}")
                continue

        return announcements

    def _extract_company_name(self, title: str) -> str:
        """Extract company name from article title."""
        separators = [",", "—", "-", "|", ":"]
        for sep in separators:
            if sep in title:
                return title.split(sep)[0].strip()
        words = title.split()[:3]
        return " ".join(words) if words else title[:50]

    def _extract_amount(self, text: str) -> Optional[float]:
        """Extract funding amount from text."""
        patterns = [
            r"\$(\d+(?:\.\d+)?)\s*(?:million|m|M)",
            r"\$(\d+(?:,\d{3})+(?:\.\d+)?)",
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                amount_str = match.group(1).replace(",", "")
                try:
                    amount = float(amount_str)
                    if "m" in text[match.start() : match.end()].lower():
                        amount *= 1_000_000
                    return amount
                except ValueError:
                    continue
        return None


class WebScraper:
    """Fallback web scraper for sources without APIs."""

    def __init__(self):
        # Simple scraper without external dependencies for now
        pass

    async def scrape_news_site(self, url: str) -> List[Dict[str, Any]]:
        """Scrape funding news from a website."""
        logger.info(f"Scraping news site: {url}")
        await asyncio.sleep(0.1)  # Simulate async I/O
        # Return mock scrape data for demo
        return [
            {
                "url": url,
                "title": "Sample News Article",
                "content": "Startup XYZ raised $10M in Series A funding...",
                "is_funding": True,
                "extracted_amount": 10_000_000,
            }
        ]
