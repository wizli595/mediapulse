from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator

from shared.models import Article


class AbstractConsumer(ABC):
    """Contract for consuming articles from a message broker.

    A consumer does ONE thing: yield articles from a stream.
    It does not transform, store, or publish.
    """

    @abstractmethod
    def consume(self) -> Iterator[Article]:
        """Yield articles one by one from the stream."""

    @abstractmethod
    def close(self) -> None:
        """Release resources (connections, subscriptions)."""
