FROM apache/airflow:2.9.3-python3.11

USER root
RUN apt-get update && apt-get install -y --no-install-recommends libxml2-dev libxslt1-dev && rm -rf /var/lib/apt/lists/*
USER airflow

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY shared/ /opt/airflow/shared/
COPY scrapers/ /opt/airflow/scrapers/
COPY ingestion/ /opt/airflow/ingestion/
COPY storage/ /opt/airflow/storage/
COPY processing/ /opt/airflow/processing/
COPY quality/ /opt/airflow/quality/
COPY warehouse/ /opt/airflow/warehouse/
COPY scripts/ /opt/airflow/scripts/

ENV PYTHONPATH=/opt/airflow
