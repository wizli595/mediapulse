"""DAG: Process bronze articles to silver (clean, normalize, detect language).

Schedule: every hour (runs after batch_scrape).
This DAG is THIN — it only calls functions from the processing layer.
"""
from __future__ import annotations

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator


def _run_bronze_to_silver(**kwargs):
    from pathlib import Path

    from ingestion.serializers.article import bytes_to_article
    from processing.silver.pipeline import process_to_silver
    from storage.local_storage import LocalStorage

    storage = LocalStorage(Path("/data/lake"))

    bronze_keys = storage.list_keys("bronze")
    processed = 0

    for key in bronze_keys:
        raw = storage.read("bronze", key)
        article = bytes_to_article(raw)
        result = process_to_silver(article, storage)
        if result:
            processed += 1

    return {"processed": processed, "total": len(bronze_keys)}


default_args = {
    "owner": "mediapulse",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="bronze_to_silver",
    default_args=default_args,
    description="Process bronze articles to silver layer",
    schedule_interval="@hourly",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["processing", "silver"],
) as dag:
    process_task = PythonOperator(
        task_id="run_bronze_to_silver",
        python_callable=_run_bronze_to_silver,
    )
