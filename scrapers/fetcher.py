from __future__ import annotations

import requests
from bs4 import BeautifulSoup

from shared.config import config
from shared.exceptions import ScrapingError
from shared.logging import get_logger

_log = get_logger(__name__)

_SESSION: requests.Session | None = None


def _get_session() -> requests.Session:
    global _SESSION
    if _SESSION is None:
        _SESSION = requests.Session()
        _SESSION.headers.update({"User-Agent": config.scraper.user_agent})
    return _SESSION


def fetch_html(url: str, timeout: int = 15) -> str:
    """Fetch raw HTML from a URL. Raises ScrapingError on failure."""
    try:
        response = _get_session().get(url, timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.RequestException as exc:
        raise ScrapingError(f"Failed to fetch {url}: {exc}") from exc


def parse_html(html: str) -> BeautifulSoup:
    """Parse raw HTML into a BeautifulSoup tree."""
    return BeautifulSoup(html, "lxml")


def fetch_and_parse(url: str, timeout: int = 15) -> BeautifulSoup:
    """Fetch a URL and return its parsed DOM."""
    return parse_html(fetch_html(url, timeout))
