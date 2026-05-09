"""Step 2: Consume Kafka → process to Silver (clean, normalize, detect language)."""

from ingestion.consumers.kafka import KafkaConsumer
from processing.silver.pipeline import process_to_silver
from shared.logging import get_logger
from storage.minio_storage import MinIOStorage

_log = get_logger(__name__)


def main() -> None:
    storage = MinIOStorage()
    consumer = KafkaConsumer()

    _log.info("Stream consumer started, waiting for articles...")
    for article in consumer.consume():
        process_to_silver(article, storage)


if __name__ == "__main__":
    main()
