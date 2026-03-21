"""Web scraper for sources without APIs."""

import logging
from typing import List, Dict, Any, Optional
import re

logger = logging.getLogger(__name__)

try:
    import requests
    from bs4 import BeautifulSoup

    HAS_SCRAPING_LIBS = True
except ImportError:
    HAS_SCRAPING_LIBS = False
    logger.warning("requests and beautifulsoup4 not installed, web scraping disabled")


class WebScraper:
    """Scrape funding data from websites."""

    def __init__(self, user_agent: str = None):
        if not HAS_SCRAPING_LIBS:
            raise ImportError(
                "Install 'requests' and 'beautifulsoup4' to use WebScraper"
            )
        self.session = requests.Session()
        if user_agent:
            self.session.headers["User-Agent"] = user_agent
        else:
            self.session.headers["User-Agent"] = (
                "PitcheRai/1.0 (+https://github.com/your-repo)"
            )

    def scrape_news_site(
        self, url: str, selectors: Dict[str, str] = None
    ) -> Dict[str, Any]:
        """Scrape a single news page looking for funding announcements."""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            data = {
                "url": url,
                "title": soup.title.string if soup.title else "",
                "text": soup.get_text(strip=True)[:1000],  # First 1000 chars
            }

            # If selectors provided, extract specific elements
            if selectors:
                for key, selector in selectors.items():
                    elements = soup.select(selector)
                    data[key] = [el.get_text(strip=True) for el in elements]

            # Look for funding keywords in content
            text_lower = data["text"].lower()
            funding_keywords = [
                "funding",
                "raises",
                "raised",
                "investment",
                "venture capital",
            ]
            data["is_funding_news"] = any(
                keyword in text_lower for keyword in funding_keywords
            )
            data["extracted_amount"] = self._extract_amount(data["text"])

            return data

        except Exception as e:
            logger.error(f"Scraping failed for {url}: {e}")
            return {"url": url, "error": str(e)}

    def scrape_blog_list(
        self, url: str, article_selector: str = "article"
    ) -> List[Dict[str, Any]]:
        """Scrape a blog listing page and extract article summaries."""
        articles = []
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            for article in soup.select(article_selector):
                try:
                    title_elem = article.select_one("h1, h2, h3, .title")
                    link_elem = article.select_one("a")
                    excerpt_elem = article.select_one(".excerpt, .summary, p")

                    title = title_elem.get_text(strip=True) if title_elem else ""
                    link = (
                        link_elem["href"]
                        if link_elem and link_elem.has_attr("href")
                        else url
                    )
                    excerpt = excerpt_elem.get_text(strip=True) if excerpt_elem else ""

                    # Make link absolute if relative
                    if link and not link.startswith(("http://", "https://")):
                        if link.startswith("/"):
                            from urllib.parse import urljoin

                            link = urljoin(url, link)
                        else:
                            link = urljoin(url, link)

                    articles.append(
                        {
                            "title": title,
                            "link": link,
                            "excerpt": excerpt[:200],
                            "is_funding": any(
                                k in (title + excerpt).lower()
                                for k in ["funding", "raises", "investment"]
                            ),
                        }
                    )
                except Exception as e:
                    logger.debug(f"Failed to parse article: {e}")
                    continue
        except Exception as e:
            logger.error(f"Failed to scrape list page {url}: {e}")

        return articles

    def _extract_amount(self, text: str) -> Optional[float]:
        """Extract monetary amount from text."""
        patterns = [
            r"\$(\d+(?:\.\d+)?)\s*(?:million|m|M)",
            r"\$(\d+(?:,\d{3})+(?:\.\d+)?)",
            r"USD\s*(\d+(?:\.\d+)?)\s*(?:million|m)",
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
