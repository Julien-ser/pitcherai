"""RSS feed collector."""

import feedparser
import asyncio
from typing import List, Dict, Any
from datetime import datetime, timedelta
from .base import BaseCollector


class RSSCollector(BaseCollector):
    """Collector for RSS feeds from various sources."""

    FEED_URLS = {
        "techcrunch": "https://techcrunch.com/feed/",
        "venturebeat": "https://venturebeat.com/category/ai/feed/",
        "crunchbase_news": "https://news.crunchbase.com/feed/",
    }

    def __init__(self):
        self.session = None

    async def parse_feeds(self, days_back: int = 7) -> List[Dict[str, Any]]:
        """Parse all configured RSS feeds."""
        all_announcements = []
        cutoff_date = datetime.utcnow() - timedelta(days=days_back)

        for feed_name, feed_url in self.FEED_URLS.items():
            try:
                announcements = await self._parse_feed(feed_name, feed_url, cutoff_date)
                all_announcements.extend(announcements)
            except Exception:
                continue

        return all_announcements

    async def _parse_feed(
        self, feed_name: str, feed_url: str, cutoff_date: datetime
    ) -> List[Dict[str, Any]]:
        """Parse a single RSS feed."""
        loop = asyncio.get_event_loop()
        feed = await loop.run_in_executor(None, feedparser.parse, feed_url)

        announcements = []
        for entry in feed.entries[:50]:  # Limit to recent 50 entries
            try:
                published = entry.get("published_parsed") or entry.get("updated_parsed")
                if published:
                    pub_date = datetime(*published[:6])
                    if pub_date < cutoff_date:
                        continue
                else:
                    continue

                # Simple heuristic to detect funding announcements
                title = entry.get("title", "").lower()
                summary = entry.get("summary", entry.get("description", "")).lower()

                funding_keywords = ["funding", "raises", "investment", "vc", "venture"]
                if any(
                    keyword in title or keyword in summary
                    for keyword in funding_keywords
                ):
                    announcement = {
                        "id": f"rss_{feed_name}_{entry.get('id', id(entry))}",
                        "source": "rss",
                        "company_name": entry.get("title", "")[:100],
                        "company_url": entry.get("link", ""),
                        "funding_amount": None,  # Would need NLP to extract
                        "funding_round": None,
                        "announcement_date": pub_date.isoformat(),
                        "investors": [],  # Would need NLP to extract
                        "industry": self._guess_industry(title, summary),
                        "stage": "unknown",
                        "metadata": {
                            "feed_name": feed_name,
                            "summary": entry.get("summary", "")[:500],
                        },
                    }
                    announcements.append(announcement)
            except Exception:
                continue

        return announcements

    def _guess_industry(self, title: str, summary: str) -> str:
        """Guess industry based on keywords."""
        text = (title + " " + summary).lower()
        industries = {
            "ai": ["ai", "artificial intelligence", "machine learning", "ml"],
            "fintech": ["fintech", "finance", "banking", "payment"],
            "healthcare": ["healthcare", "health", "medical", "biotech"],
            "saas": ["saas", "software", "cloud", "platform"],
            "ecommerce": ["ecommerce", "e-commerce", "retail", "shopping"],
        }

        for industry, keywords in industries.items():
            if any(keyword in text for keyword in keywords):
                return industry
        return "technology"

    def get_recent_funding_rounds(self, days_back: int = 7) -> List[Dict[str, Any]]:
        """Synchronous version - runs parser in event loop."""
        return asyncio.run(self.parse_feeds(days_back))

    def get_investor_details(self, investor_id: str) -> Dict[str, Any]:
        """Not supported for RSS."""
        return None

    def search_investors(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Not supported for RSS."""
        return []
