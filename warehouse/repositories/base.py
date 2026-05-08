from __future__ import annotations

from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    """Base class for warehouse repositories.

    Each repository handles CRUD for one table.
    It receives a connection — it does not create one.
    """

    def __init__(self, conn) -> None:
        self._conn = conn

    def _execute(self, query: str, params: tuple = ()) -> None:
        with self._conn.cursor() as cur:
            cur.execute(query, params)

    def _fetch_all(self, query: str, params: tuple = ()) -> list[tuple]:
        with self._conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()

    def _fetch_one(self, query: str, params: tuple = ()) -> tuple | None:
        with self._conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchone()

    @abstractmethod
    def create_table(self) -> None:
        """Ensure the table exists."""
