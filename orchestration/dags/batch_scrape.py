"""DAG: Scrape all news sources and publish articles to Kafka / file.

Schedule: every hour.
This DAG is THIN — it only calls functions from the scraping and ingestion layers.
"""
from __future__ import annotations

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator


def _run_batch_scrape(**kwargs):
    from pathlib import Path

    from ingestion.publishers.file import FilePublisher
    from processing.bronze.raw_writer import write_raw_article
    from quality.validator import validate_article
    from scrapers.runner import run_all_spiders
    from storage.local_storage import LocalStorage

    articles = run_all_spiders()

    storage = LocalStorage(Path("/data/lake"))
    publisher = FilePublisher(Path("/data/raw_articles.jsonl"))

    for article in articles:
        report = validate_article(article)
        if not report.passed:
            continue
        write_raw_article(article, storage)
        publisher.publish(article)

    publisher.close()


default_args = {
    "owner": "mediapulse",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="batch_scrape",
    default_args=default_args,
    description="Scrape all news sources every hour",
    schedule_interval="@hourly",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["scraping", "ingestion"],
) as dag:
    scrape_task = PythonOperator(
        task_id="run_batch_scrape",
        python_callable=_run_batch_scrape,
    )
