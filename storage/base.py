from __future__ import annotations

from abc import ABC, abstractmethod


class AbstractStorage(ABC):
    """Contract for Data Lake storage.

    A storage backend does ONE thing: read/write/list objects in layers.
    It does not transform, validate, or publish.
    Layer names map to medallion tiers: 'bronze', 'silver', 'gold'.
    """

    @abstractmethod
    def write(self, layer: str, key: str, data: bytes) -> None:
        """Write a single object to a layer."""

    @abstractmethod
    def read(self, layer: str, key: str) -> bytes:
        """Read a single object from a layer."""

    @abstractmethod
    def list_keys(self, layer: str, prefix: str = "") -> list[str]:
        """List all object keys in a layer, optionally filtered by prefix."""

    @abstractmethod
    def exists(self, layer: str, key: str) -> bool:
        """Check if an object exists in a layer."""

    @abstractmethod
    def delete(self, layer: str, key: str) -> None:
        """Delete a single object from a layer."""
