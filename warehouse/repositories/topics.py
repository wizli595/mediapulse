from __future__ import annotations

from processing.gold.topic_extractor import TopicRecord
from warehouse.repositories.base import AbstractRepository


class TopicRepository(AbstractRepository):

    def create_table(self) -> None:
        self._execute("""
            CREATE TABLE IF NOT EXISTS topics (
                id         SERIAL PRIMARY KEY,
                keyword    TEXT NOT NULL,
                frequency  INTEGER NOT NULL,
                updated_at TIMESTAMP DEFAULT NOW()
            )
        """)
        self._conn.commit()

    def replace_all(self, records: list[TopicRecord]) -> None:
        """Clear and reload all topic records (full refresh)."""
        self._execute("DELETE FROM topics")
        for r in records:
            self._execute(
                "INSERT INTO topics (keyword, frequency) VALUES (%s, %s)",
                (r.keyword, r.frequency),
            )
        self._conn.commit()

    def get_top(self, limit: int = 50) -> list[tuple]:
        return self._fetch_all("SELECT keyword, frequency FROM topics ORDER BY frequency DESC LIMIT %s", (limit,))
