"""Step 4: Load Gold analytics into PostgreSQL warehouse."""

import json

from ingestion.serializers.article import bytes_to_article
from processing.gold.topic_extractor import TopicRecord
from processing.gold.trend_aggregator import TrendRecord
from shared.logging import get_logger
from storage.minio_storage import MinIOStorage
from warehouse.connection import get_connection
from warehouse.repositories.articles import ArticleRepository
from warehouse.repositories.topics import TopicRepository
from warehouse.repositories.trends import TrendRepository

_log = get_logger(__name__)


def main() -> None:
    storage = MinIOStorage()
    conn = get_connection()

    # Load articles from silver
    article_repo = ArticleRepository(conn)
    article_repo.create_table()
    silver_keys = storage.list_keys("silver")
    for key in silver_keys:
        article = bytes_to_article(storage.read("silver", key))
        article_repo.upsert(article)
    _log.info("Loaded %d articles into warehouse", len(silver_keys))

    # Load trends
    if storage.exists("gold", "trends.json"):
        trend_repo = TrendRepository(conn)
        trend_repo.create_table()
        for r in json.loads(storage.read("gold", "trends.json")):
            trend_repo.upsert(TrendRecord(**r))
        _log.info("Loaded trends into warehouse")

    # Load topics
    if storage.exists("gold", "topics.json"):
        topic_repo = TopicRepository(conn)
        topic_repo.create_table()
        records = [TopicRecord(**r) for r in json.loads(storage.read("gold", "topics.json"))]
        topic_repo.replace_all(records)
        _log.info("Loaded %d topics into warehouse", len(records))

    conn.close()
    _log.info("Warehouse load complete")


if __name__ == "__main__":
    main()
