from __future__ import annotations

from scrapers.base import AbstractSpider
from scrapers.spiders.akhbarona import AkhbaronaSpider
from scrapers.spiders.aljazeera import AlJazeeraSpider
from scrapers.spiders.barlamane import BarlamaneSpider
from scrapers.spiders.bbc import BBCSpider
from scrapers.spiders.cnn import CNNSpider
from scrapers.spiders.hespress import HespressSpider
from scrapers.spiders.lakom import LakomSpider
from scrapers.spiders.reuters import ReutersSpider

_SPIDERS: list[type[AbstractSpider]] = [
    HespressSpider,
    AkhbaronaSpider,
    LakomSpider,
    BarlamaneSpider,
    AlJazeeraSpider,
    BBCSpider,
    CNNSpider,
    ReutersSpider,
]


def get_all_spiders() -> list[AbstractSpider]:
    """Return an instance of every registered spider."""
    return [cls() for cls in _SPIDERS]


def get_spider_by_name(name: str) -> AbstractSpider | None:
    """Look up a spider by its source name. Returns None if not found."""
    for cls in _SPIDERS:
        spider = cls()
        if spider.name == name:
            return spider
    return None
