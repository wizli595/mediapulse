"""Step 1: Scrape all sources → validate → write to Bronze → publish to Kafka."""

from ingestion.publishers.kafka import KafkaPublisher
from processing.bronze.raw_writer import write_raw_article
from quality.validator import validate_article
from scrapers.runner import run_all_spiders
from shared.logging import get_logger
from storage.minio_storage import MinIOStorage

_log = get_logger(__name__)


def main() -> None:
    storage = MinIOStorage()
    publisher = KafkaPublisher()

    articles = run_all_spiders()
    published = 0

    for article in articles:
        report = validate_article(article)
        if report.passed:
            write_raw_article(article, storage)
            publisher.publish(article)
            published += 1

    publisher.close()
    _log.info("Batch scrape done: %d/%d articles published", published, len(articles))


if __name__ == "__main__":
    main()
