from __future__ import annotations

from abc import ABC, abstractmethod

from shared.models import Article


class AbstractPublisher(ABC):
    """Contract for publishing articles to a message broker.

    A publisher does ONE thing: send an article somewhere.
    It does not scrape, transform, or store.
    """

    @abstractmethod
    def publish(self, article: Article) -> None:
        """Publish a single article."""

    @abstractmethod
    def close(self) -> None:
        """Release resources (connections, file handles)."""
