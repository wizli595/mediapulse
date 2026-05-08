from shared.config import config, MinioConfig, KafkaConfig, PostgresConfig, ScraperConfig


def test_config_has_all_sections():
    assert isinstance(config.minio, MinioConfig)
    assert isinstance(config.kafka, KafkaConfig)
    assert isinstance(config.postgres, PostgresConfig)
    assert isinstance(config.scraper, ScraperConfig)


def test_minio_defaults():
    assert config.minio.bucket_bronze == "bronze"
    assert config.minio.bucket_silver == "silver"
    assert config.minio.bucket_gold == "gold"


def test_kafka_defaults():
    assert config.kafka.topic_raw_articles == "raw-articles"


def test_postgres_dsn():
    dsn = config.postgres.dsn
    assert dsn.startswith("postgresql://")
    assert str(config.postgres.port) in dsn
