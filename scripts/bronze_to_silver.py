"""Step 2 (batch): Read all Bronze articles → process to Silver."""

from ingestion.serializers.article import bytes_to_article
from processing.silver.pipeline import process_to_silver
from shared.logging import get_logger
from storage.minio_storage import MinIOStorage

_log = get_logger(__name__)


def main() -> None:
    storage = MinIOStorage()
    keys = storage.list_keys("bronze")
    processed = 0

    for key in keys:
        article = bytes_to_article(storage.read("bronze", key))
        if process_to_silver(article, storage):
            processed += 1

    _log.info("Bronze to Silver done: %d/%d articles processed", processed, len(keys))


if __name__ == "__main__":
    main()
