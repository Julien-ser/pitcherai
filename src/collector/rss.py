"""RSS feed collector for press releases."""

import feedparser
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime, timedelta
import re

logger = logging.getLogger(__name__)


class RSSCollector:
    """Collect funding news from RSS feeds."""

    def __init__(self, feed_urls: List[str] = None):
        self.feed_urls = feed_urls or [
            "https://techcrunch.com/feed/",
            "https://feeds.feedburner.com/venturebeat/tech",
        ]

    def parse_feeds(self, days_back: int = 7) -> List[Dict[str, Any]]:
        """Parse all configured RSS feeds for funding announcements."""
        logger.info(f"Parsing {len(self.feed_urls)} RSS feeds for funding news")

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

                    # Detect funding announcements with keywords
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

        logger.info(f"Found {len(announcements)} funding announcements from RSS")
        return announcements

    def _extract_company_name(self, title: str) -> str:
        """Extract company name from article title."""
        # Basic extraction: look for pattern like "Company X raises..."
        separators = [",", "—", "-", "|", ":"]
        for sep in separators:
            if sep in title:
                return title.split(sep)[0].strip()
        # If no separator, take first few words
        words = title.split()[:3]
        return " ".join(words) if words else title[:50]

    def _extract_amount(self, text: str) -> Optional[float]:
        """Extract funding amount from text."""
        patterns = [
            r"\$(\d+(?:\.\d+)?)\s*(?:million|m|M)",  # $15M or $15 million
            r"\$(\d+(?:,\d{3})+(?:\.\d+)?)",  # $1,000,000
            r"USD\s*(\d+(?:\.\d+)?)\s*(?:million|m)",  # USD 15 million
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
