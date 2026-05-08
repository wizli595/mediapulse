from __future__ import annotations

from processing.gold.trend_aggregator import TrendRecord
from warehouse.repositories.base import AbstractRepository


class TrendRepository(AbstractRepository):

    def create_table(self) -> None:
        self._execute("""
            CREATE TABLE IF NOT EXISTS trends (
                id             SERIAL PRIMARY KEY,
                date           DATE NOT NULL,
                source         VARCHAR(50) NOT NULL,
                category       TEXT,
                article_count  INTEGER NOT NULL,
                UNIQUE (date, source, category)
            )
        """)
        self._conn.commit()

    def upsert(self, record: TrendRecord) -> None:
        self._execute(
            """
            INSERT INTO trends (date, source, category, article_count)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (date, source, category) DO UPDATE SET
                article_count = EXCLUDED.article_count
            """,
            (record.date, record.source, record.category, record.article_count),
        )
        self._conn.commit()

    def get_all(self) -> list[tuple]:
        return self._fetch_all("SELECT date, source, category, article_count FROM trends ORDER BY date DESC")
