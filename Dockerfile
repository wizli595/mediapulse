FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY shared/ shared/
COPY scrapers/ scrapers/
COPY ingestion/ ingestion/
COPY storage/ storage/
COPY processing/ processing/
COPY quality/ quality/
COPY warehouse/ warehouse/
COPY scripts/ scripts/

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
