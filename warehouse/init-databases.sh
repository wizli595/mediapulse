#!/bin/bash
set -e

# Create additional databases for Airflow and Metabase
# The main database ($POSTGRES_DB) is created automatically by the postgres image

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE airflow;
    CREATE DATABASE metabase;
EOSQL
