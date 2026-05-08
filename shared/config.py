from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_PROJECT_ROOT / ".env")


def _env(key: str, default: str = "") -> str:
    return os.getenv(key, default)


def _env_int(key: str, default: int = 0) -> int:
    return int(os.getenv(key, str(default)))


@dataclass(frozen=True)
class MinioConfig:
    endpoint: str = _env("MINIO_ENDPOINT", "minio:9000")
    access_key: str = _env("MINIO_ROOT_USER", "mediapulse")
    secret_key: str = _env("MINIO_ROOT_PASSWORD", "changeme123")
    bucket_bronze: str = _env("MINIO_BUCKET_BRONZE", "bronze")
    bucket_silver: str = _env("MINIO_BUCKET_SILVER", "silver")
    bucket_gold: str = _env("MINIO_BUCKET_GOLD", "gold")
    secure: bool = False


@dataclass(frozen=True)
class KafkaConfig:
    bootstrap_servers: str = _env("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
    topic_raw_articles: str = _env("KAFKA_TOPIC_RAW_ARTICLES", "raw-articles")


@dataclass(frozen=True)
class PostgresConfig:
    host: str = _env("POSTGRES_HOST", "postgres")
    port: int = _env_int("POSTGRES_PORT", 5432)
    database: str = _env("POSTGRES_DB", "mediapulse")
    user: str = _env("POSTGRES_USER", "mediapulse")
    password: str = _env("POSTGRES_PASSWORD", "changeme123")

    @property
    def dsn(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


@dataclass(frozen=True)
class ScraperConfig:
    interval_hours: int = _env_int("SCRAPE_INTERVAL_HOURS", 1)
    user_agent: str = _env("SCRAPE_USER_AGENT", "MediaPulse/1.0 (Academic Research Project)")


@dataclass(frozen=True)
class Config:
    minio: MinioConfig = MinioConfig()
    kafka: KafkaConfig = KafkaConfig()
    postgres: PostgresConfig = PostgresConfig()
    scraper: ScraperConfig = ScraperConfig()


# Singleton — import this everywhere
config = Config()
