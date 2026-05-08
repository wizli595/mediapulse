"""DAG: Load gold analytics into PostgreSQL warehouse.

Schedule: every 2 hours (runs after silver_to_gold).
This DAG is THIN — it only calls functions from the warehouse layer.
"""
from __future__ import annotations

import json
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator


def _run_gold_to_warehouse(**kwargs):
    from pathlib import Path

    from processing.gold.source_counter import SourceCount
    from processing.gold.topic_extractor import TopicRecord
    from processing.gold.trend_aggregator import TrendRecord
    from storage.local_storage import LocalStorage
    from warehouse.connection import get_connection
    from warehouse.repositories.articles import ArticleRepository
    from warehouse.repositories.topics import TopicRepository
    from warehouse.repositories.trends import TrendRepository

    storage = LocalStorage(Path("/data/lake"))
    conn = get_connection()

    # Ensure tables exist
    ArticleRepository(conn).create_table()
    TrendRepository(conn).create_table()
    TopicRepository(conn).create_table()

    # Load trends
    if storage.exists("gold", "trends.json"):
        data = json.loads(storage.read("gold", "trends.json"))
        repo = TrendRepository(conn)
        for row in data:
            repo.upsert(TrendRecord(
                date=row["date"], source=row["source"],
                category=row["category"], article_count=row["article_count"],
            ))

    # Load topics
    if storage.exists("gold", "topics.json"):
        data = json.loads(storage.read("gold", "topics.json"))
        repo = TopicRepository(conn)
        repo.replace_all([TopicRecord(keyword=r["keyword"], frequency=r["frequency"]) for r in data])

    conn.close()


default_args = {
    "owner": "mediapulse",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="gold_to_warehouse",
    default_args=default_args,
    description="Load gold analytics into PostgreSQL",
    schedule_interval="0 */2 * * *",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["warehouse", "loading"],
) as dag:
    load_task = PythonOperator(
        task_id="run_gold_to_warehouse",
        python_callable=_run_gold_to_warehouse,
    )
