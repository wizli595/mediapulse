"""DAG: Aggregate silver articles into gold analytics.

Schedule: every 2 hours.
This DAG is THIN — it only calls functions from the processing layer.
"""
from __future__ import annotations

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator


def _run_silver_to_gold(**kwargs):
    from pathlib import Path

    from ingestion.serializers.article import bytes_to_article
    from processing.gold.pipeline import process_to_gold
    from storage.local_storage import LocalStorage

    storage = LocalStorage(Path("/data/lake"))

    silver_keys = storage.list_keys("silver")
    articles = []

    for key in silver_keys:
        raw = storage.read("silver", key)
        articles.append(bytes_to_article(raw))

    process_to_gold(articles, storage)

    return {"articles_aggregated": len(articles)}


default_args = {
    "owner": "mediapulse",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="silver_to_gold",
    default_args=default_args,
    description="Aggregate silver articles into gold analytics",
    schedule_interval="0 */2 * * *",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["processing", "gold"],
) as dag:
    aggregate_task = PythonOperator(
        task_id="run_silver_to_gold",
        python_callable=_run_silver_to_gold,
    )
