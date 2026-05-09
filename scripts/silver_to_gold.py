"""Step 3: Read all Silver articles → aggregate into Gold."""

from ingestion.serializers.article import bytes_to_article
from processing.gold.pipeline import process_to_gold
from shared.logging import get_logger
from storage.minio_storage import MinIOStorage

_log = get_logger(__name__)


def main() -> None:
    storage = MinIOStorage()
    keys = storage.list_keys("silver")
    articles = [bytes_to_article(storage.read("silver", k)) for k in keys]

    process_to_gold(articles, storage)
    _log.info("Silver to Gold done: %d articles aggregated", len(articles))


if __name__ == "__main__":
    main()
