from __future__ import annotations

from shared.models import Article
from warehouse.repositories.base import AbstractRepository


class ArticleRepository(AbstractRepository):

    def create_table(self) -> None:
        self._execute("""
            CREATE TABLE IF NOT EXISTS articles (
                article_id    VARCHAR(16) PRIMARY KEY,
                title         TEXT NOT NULL,
                author        TEXT,
                published_at  TIMESTAMP NOT NULL,
                category      TEXT,
                content       TEXT NOT NULL,
                source        VARCHAR(50) NOT NULL,
                url           TEXT NOT NULL UNIQUE,
                language      VARCHAR(10),
                scraped_at    TIMESTAMP NOT NULL
            )
        """)
        self._conn.commit()

    def upsert(self, article: Article) -> None:
        self._execute(
            """
            INSERT INTO articles (article_id, title, author, published_at, category, content, source, url, language, scraped_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (article_id) DO UPDATE SET
                title = EXCLUDED.title,
                author = EXCLUDED.author,
                category = EXCLUDED.category,
                content = EXCLUDED.content,
                language = EXCLUDED.language,
                scraped_at = EXCLUDED.scraped_at
            """,
            (
                article.article_id,
                article.title,
                article.author,
                article.published_at,
                article.category,
                article.content,
                article.source,
                article.url,
                article.language,
                article.scraped_at,
            ),
        )
        self._conn.commit()

    def get_by_id(self, article_id: str) -> tuple | None:
        return self._fetch_one("SELECT * FROM articles WHERE article_id = %s", (article_id,))

    def count_by_source(self) -> list[tuple]:
        return self._fetch_all(
            "SELECT source, COUNT(*) FROM articles GROUP BY source ORDER BY COUNT(*) DESC"
        )

    def count_by_day(self) -> list[tuple]:
        return self._fetch_all(
            "SELECT DATE(published_at), COUNT(*) FROM articles GROUP BY DATE(published_at) ORDER BY DATE(published_at) DESC"
        )
