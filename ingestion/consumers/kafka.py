from __future__ import annotations

from collections.abc import Iterator

from kafka import KafkaConsumer as _KafkaConsumer

from ingestion.consumers.base import AbstractConsumer
from ingestion.serializers.article import bytes_to_article
from shared.config import config
from shared.exceptions import IngestionError
from shared.logging import get_logger
from shared.models import Article

_log = get_logger(__name__)


class KafkaConsumer(AbstractConsumer):

    def __init__(self, group_id: str = "mediapulse-consumer") -> None:
        try:
            self._consumer = _KafkaConsumer(
                config.kafka.topic_raw_articles,
                bootstrap_servers=config.kafka.bootstrap_servers,
                group_id=group_id,
                auto_offset_reset="earliest",
                enable_auto_commit=True,
                value_deserializer=lambda v: v,
            )
        except Exception as exc:
            raise IngestionError(f"Failed to connect to Kafka: {exc}") from exc

    def consume(self) -> Iterator[Article]:
        _log.info("Consuming from topic: %s", config.kafka.topic_raw_articles)
        for message in self._consumer:
            try:
                article = bytes_to_article(message.value)
                _log.info("Consumed article %s", article.article_id)
                yield article
            except Exception:
                _log.exception("Failed to deserialize message at offset %d", message.offset)

    def close(self) -> None:
        self._consumer.close()
        _log.info("Kafka consumer closed")
