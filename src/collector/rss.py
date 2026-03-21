"""RSS feed collector for press releases."""

import feedparser
from typing import List
import logging

logger = logging.getLogger(__name__)


class RSSCollector:
    """Collect funding news from RSS feeds."""

    def __init__(self, feed_urls: List[str]):
        self.feed_urls = feed_urls

    def parse_feeds(self) -> List[dict]:
        """Parse all configured RSS feeds."""
        articles = []
        for url in self.feed_urls:
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries:
                    articles.append(
                        {
                            "title": entry.get("title", ""),
                            "link": entry.get("link", ""),
                            "published": entry.get("published", ""),
                            "summary": entry.get("summary", ""),
                        }
                    )
            except Exception as e:
                logger.error(f"Failed to parse RSS feed {url}: {e}")
        return articles
