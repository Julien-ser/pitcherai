"""Web scraper for sources without APIs."""

import requests
from bs4 import BeautifulSoup
from typing import List
import logging

logger = logging.getLogger(__name__)


class WebScraper:
    """Scrape funding data from websites."""

    def __init__(self, user_agent: str = None):
        self.session = requests.Session()
        if user_agent:
            self.session.headers["User-Agent"] = user_agent

    def scrape_page(self, url: str, selectors: dict) -> dict:
        """Scrape a single page using CSS selectors."""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            data = {}
            for key, selector in selectors.items():
                element = soup.select_one(selector)
                data[key] = element.get_text(strip=True) if element else None
            return data
        except Exception as e:
            logger.error(f"Scraping failed for {url}: {e}")
            return {}
