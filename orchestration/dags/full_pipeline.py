"""DAG: Full MediaPulse pipeline — Scrape → Bronze → Silver → Gold → Warehouse.

Single DAG with 4 chained tasks using MinIO + Kafka + PostgreSQL.
Trigger manually from the Airflow UI to run the complete pipeline.
"""
from __future__ import annotations

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator


def _step1_scrape(**kwargs):
    from scripts.batch_scrape import main
    main()


def _step2_bronze_to_silver(**kwargs):
    from scripts.bronze_to_silver import main
    main()


def _step3_silver_to_gold(**kwargs):
    from scripts.silver_to_gold import main
    main()


def _step4_gold_to_warehouse(**kwargs):
    from scripts.gold_to_warehouse import main
    main()


default_args = {
    "owner": "mediapulse",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="full_pipeline",
    default_args=default_args,
    description="Full pipeline: Scrape → Bronze → Silver → Gold → Warehouse",
    schedule_interval=None,
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["pipeline", "full"],
) as dag:
    scrape = PythonOperator(task_id="scrape_to_bronze", python_callable=_step1_scrape)
    silver = PythonOperator(task_id="bronze_to_silver", python_callable=_step2_bronze_to_silver)
    gold = PythonOperator(task_id="silver_to_gold", python_callable=_step3_silver_to_gold)
    warehouse = PythonOperator(task_id="gold_to_warehouse", python_callable=_step4_gold_to_warehouse)

    scrape >> silver >> gold >> warehouse
