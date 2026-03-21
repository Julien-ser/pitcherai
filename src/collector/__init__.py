"""Data collection module for funding announcements."""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Any, List, Optional, Dict
import re
import feedparser
import httpx

from src.models import Investor, Startup

logger = logging.getLogger(__name__)


class CrunchbaseCollector:
    """Collect funding data from Crunchbase API."""

    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.base_url = "https://api.crunchbase.com/v3"
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

        # Real Crunchbase API integration
        try:
            # Calculate date filter
            cutoff_date = (datetime.now() - timedelta(days=days_back)).strftime(
                "%Y-%m-%d"
            )

            # Crunchbase API v3 endpoints
            # Using the funding-rounds endpoint with date filters
            url = f"{self.base_url}/funding-rounds"
            params = {
                "updated_at_min": cutoff_date,
                "sort": "updated_at DESC",
                "limit": 100,
            }
            headers = {
                "X-cb-user-key": self.api_key,
                "Content-Type": "application/json",
            }

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, params=params, headers=headers)
                response.raise_for_status()
                data = response.json()

            # Parse Crunchbase response into our format
            rounds = []
            for item in data.get("data", {}).get("items", []):
                funding_round = item.get("properties", {})

                # Extract company information
                company = funding_round.get("company", {})
                company_name = company.get("properties", {}).get(
                    "name", "Unknown Company"
                )
                industry = self._extract_industry(company)

                # Extract investors
                investor_ids = []
                for investor in funding_round.get("investors", []):
                    inv_props = investor.get("properties", {})
                    inv_id = inv_props.get("uuid", inv_props.get("name", ""))
                    investor_ids.append(inv_id)

                round_data = {
                    "id": funding_round.get("uuid", f"round_{len(rounds)}"),
                    "company_name": company_name,
                    "industry": industry,
                    "stage": funding_round.get("stage", {}).get("value", ""),
                    "amount": funding_round.get("money_raised", 0),
                    "date": funding_round.get("updated_at", ""),
                    "investor_ids": investor_ids,
                }
                rounds.append(round_data)

            logger.info(
                f"Successfully fetched {len(rounds)} funding rounds from Crunchbase"
            )
            return rounds

        except httpx.HTTPError as e:
            logger.error(f"Crunchbase API HTTP error: {e}")
            return []
        except Exception as e:
            logger.error(f"Crunchbase API error: {e}")
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

        # Real Crunchbase API integration
        try:
            # First, determine if this is a person or organization
            # Try fetching as person first
            url = f"{self.base_url}/people/{investor_id}"
            headers = {
                "X-cb-user-key": self.api_key,
                "Content-Type": "application/json",
            }

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, headers=headers)

                if response.status_code == 404:
                    # Try as organization
                    url = f"{self.base_url}/organizations/{investor_id}"
                    response = await client.get(url, headers=headers)

                response.raise_for_status()
                data = response.json()

            properties = data.get("data", {}).get("properties", {})

            # Extract investor details
            investor = Investor(
                id=investor_id,
                name=properties.get("name", "Unknown Investor"),
                email="",  # Crunchbase doesn't typically provide direct email
                firm=properties.get("name", ""),  # Use name as firm for now
                focus_areas=self._extract_focus_areas(properties),
                stage_preference=self._extract_stage_preferences(properties),
                portfolio=[],  # Would need separate API calls
                recent_investments=[],  # Would need separate API calls
                connections=[],  # Would need LinkedIn integration
                location=properties.get("location", {}).get("value", "")
                if properties.get("location")
                else None,
                check_size_min=properties.get("min_investment"),
                check_size_max=properties.get("max_investment"),
                website=properties.get("website", {}).get("value", "")
                if properties.get("website")
                else None,
            )

            logger.info(f"Successfully fetched investor details for {investor_id}")
            return investor

        except httpx.HTTPError as e:
            logger.error(f"Crunchbase API HTTP error fetching investor: {e}")
            return None
        except Exception as e:
            logger.error(f"Crunchbase API error fetching investor: {e}")
            return None

    def _extract_focus_areas(self, properties: dict) -> List[str]:
        """Extract focus areas from Crunchbase properties."""
        focus_areas = []
        categories = properties.get("category", [])
        for cat in categories:
            if isinstance(cat, dict):
                focus_areas.append(cat.get("value", cat.get("name", "")))
        return focus_areas if focus_areas else ["Unknown"]

    def _extract_stage_preferences(self, properties: dict) -> List[str]:
        """Extract investment stage preferences."""
        # Crunchbase may have investment stage info
        stages = properties.get("investment_stage", [])
        if stages:
            return [s.get("value", s) if isinstance(s, dict) else s for s in stages]
        # Default stages based on investor type
        return ["seed", "series-a", "series-b"]

    def _extract_industry(self, company: dict) -> str:
        """Extract industry from company data."""
        # Crunchbase category/value extraction
        if isinstance(company, dict):
            categories = company.get("properties", {}).get("category", [])
            if categories:
                # Return first category name
                for cat in categories:
                    if isinstance(cat, dict):
                        return cat.get("value", cat.get("name", "Unknown"))
            # Try industry field
            industry = company.get("properties", {}).get("industry", "")
            if industry:
                return industry
        return "Unknown"


class AngelListCollector:
    """Collect funding data from AngelList."""

    def __init__(self, access_token: str = None):
        self.access_token = access_token
        self.base_url = "https://api.angel.co/1"
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

        # Real AngelList API integration
        try:
            url = f"{self.base_url}/startups"
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            }
            # AngelList API doesn't have a direct "recently funded" endpoint,
            # so we fetch startups with recent updates and filter for funding news
            params = {
                "filter": "raised_funding",  # If supported by API
                "sort": "updated_at DESC",
                "per_page": 100,
            }

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, params=params, headers=headers)
                response.raise_for_status()
                data = response.json()

            # Parse AngelList response
            startups = []
            for item in data.get("startups", []):
                startup = item.get("startup", {})
                startup_data = {
                    "id": startup.get("id", f"startup_al_{len(startups)}"),
                    "name": startup.get("name", "Unknown Startup"),
                    "industry": startup.get("markets", [{}])[0].get("name", "Tech")
                    if startup.get("markets")
                    else "Tech",
                    "stage": startup.get("stage", ""),
                    "description": startup.get(
                        "tagline", startup.get("description", "")
                    ),
                    "funding_needed": startup.get("funding_needed", 0),
                    "location": startup.get("location", {}).get("name", "")
                    if startup.get("location")
                    else "",
                    "website": startup.get("company_url", ""),
                    "founders": [
                        f"{f.get('first_name', '')} {f.get('last_name', '')}".strip()
                        for f in startup.get("founders", [])
                    ],
                }
                startups.append(startup_data)

            logger.info(f"Successfully fetched {len(startups)} startups from AngelList")
            return startups

        except httpx.HTTPError as e:
            logger.error(f"AngelList API HTTP error: {e}")
            return []
        except Exception as e:
            logger.error(f"AngelList API error: {e}")
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

        # Real AngelList API integration
        try:
            url = f"{self.base_url}/funding_announcements"
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            }
            params = {
                "sort": "created_at DESC",
                "per_page": 100,
            }

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, params=params, headers=headers)
                response.raise_for_status()
                data = response.json()

            # Parse AngelList response
            announcements = []
            for item in data.get("funding_announcements", []):
                announcement = item.get("funding_announcement", {})
                startup = announcement.get("startup", {})

                # Extract investor IDs from the announcement
                investor_ids = []
                for investor in announcement.get("investors", []):
                    investor_ids.append(str(investor.get("id", "")))

                announcement_data = {
                    "id": str(announcement.get("id", f"ann_{len(announcements)}")),
                    "company_id": str(startup.get("id", "")),
                    "company_name": startup.get("name", "Unknown Company"),
                    "industry": startup.get("markets", [{}])[0].get("name", "Tech")
                    if startup.get("markets")
                    else "Tech",
                    "stage": startup.get("stage", ""),
                    "amount": announcement.get("amount_raised", 0),
                    "date": announcement.get("created_at", ""),
                    "investor_ids": investor_ids,
                }
                announcements.append(announcement_data)

            logger.info(
                f"Successfully fetched {len(announcements)} funding announcements from AngelList"
            )
            return announcements

        except httpx.HTTPError as e:
            logger.error(f"AngelList API HTTP error: {e}")
            return []
        except Exception as e:
            logger.error(f"AngelList API error: {e}")
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

        # Real AngelList API integration
        try:
            url = f"{self.base_url}/investors"
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            }
            params = {
                "per_page": 100,
            }

            # Add filters based on criteria
            if "industry" in criteria:
                params["markets"] = criteria["industry"]
            if "stage" in criteria:
                params["investment_stage"] = criteria["stage"]
            if "location" in criteria:
                params["location"] = criteria["location"]

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, params=params, headers=headers)
                response.raise_for_status()
                data = response.json()

            # Parse AngelList response into Investor models
            investors = []
            for item in data.get("investors", []):
                inv_data = item.get("investor", {})

                # Extract focus areas from markets
                focus_areas = []
                for market in inv_data.get("markets", []):
                    if isinstance(market, dict):
                        focus_areas.append(market.get("name", ""))
                    elif isinstance(market, str):
                        focus_areas.append(market)

                # Extract stage preferences
                stage_preference = []
                for stage in inv_data.get("investment_stage", []):
                    if isinstance(stage, dict):
                        stage_preference.append(stage.get("value", ""))
                    elif isinstance(stage, str):
                        stage_preference.append(stage)

                investor = Investor(
                    id=str(inv_data.get("id", f"inv_al_{len(investors)}")),
                    name=inv_data.get("name", "Unknown Investor"),
                    email=inv_data.get("email", ""),
                    firm=inv_data.get("company", {}).get("name", "")
                    if inv_data.get("company")
                    else inv_data.get("name", ""),
                    focus_areas=focus_areas or [],
                    stage_preference=stage_preference or [],
                    portfolio=[],  # Would need separate API call to get portfolio
                    recent_investments=[],  # Would need separate API call
                    connections=[],  # Would need LinkedIn integration
                    location=inv_data.get("location", {}).get("name", "")
                    if inv_data.get("location")
                    else None,
                    check_size_min=inv_data.get("min_investment"),
                    check_size_max=inv_data.get("max_investment"),
                    website=inv_data.get("angellist_url", ""),
                )
                investors.append(investor)

            logger.info(
                f"Successfully fetched {len(investors)} investors from AngelList"
            )
            return investors

        except httpx.HTTPError as e:
            logger.error(f"AngelList API HTTP error: {e}")
            return []
        except Exception as e:
            logger.error(f"AngelList API error: {e}")
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
