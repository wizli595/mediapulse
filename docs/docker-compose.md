# Docker Compose — Services

Le fichier `docker-compose.yml` définit 16 services répartis en 5 catégories.

## Infrastructure (4 services)

### zookeeper
- **Image** : `confluentinc/cp-zookeeper:7.6.0`
- **Rôle** : Coordination du cluster Kafka
- **Port interne** : 2181
- **Volume** : `zookeeper-data`

### kafka
- **Image** : `confluentinc/cp-kafka:7.6.0`
- **Rôle** : Broker de messages pour l'ingestion streaming
- **Port** : 9092
- **Volume** : `kafka-data`
- **Dépend de** : zookeeper
- **Topics** : `raw-articles` (créé automatiquement)
- **Healthcheck** : `kafka-broker-api-versions`

### minio
- **Image** : `minio/minio:latest`
- **Rôle** : Data Lake S3-compatible (stockage Bronze/Silver/Gold)
- **Ports** : 9000 (API), 9001 (Console UI)
- **Volume** : `minio-data`
- **Variables d'environnement** :
  - `MINIO_ROOT_USER` : identifiant admin
  - `MINIO_ROOT_PASSWORD` : mot de passe admin
  - `MINIO_PROMETHEUS_AUTH_TYPE=public` : expose les métriques sans auth
- **Healthcheck** : `mc ready local`

### postgres
- **Image** : `postgres:16-alpine`
- **Rôle** : Data Warehouse + stockage Airflow + stockage Metabase
- **Port** : 5432
- **Volume** : `postgres-data`
- **Init scripts** :
  - `warehouse/init-databases.sh` : crée les bases `airflow` et `metabase`
  - `warehouse/schema.sql` : crée les tables `articles`, `trends`, `topics`, `source_counts`
- **Healthcheck** : `pg_isready`

## Application (7 services)

Tous utilisent le même `Dockerfile` de base et partagent la configuration `x-mediapulse-common`.

### init-buckets
- **Commande** : `python -m storage.setup_buckets`
- **Rôle** : Crée les buckets `bronze`, `silver`, `gold` dans MinIO
- **Exécution** : une seule fois au démarrage

### batch-scraper
- **Commande** : `python -m scripts.batch_scrape`
- **Rôle** : Scrape les 8 sources → valide → écrit Bronze → publie Kafka
- **Dépend de** : init-buckets

### stream-consumer
- **Commande** : `python -m scripts.consume_stream`
- **Rôle** : Consomme Kafka en continu → écrit Silver
- **Restart** : `always` (tourne en permanence)

### bronze-to-silver
- **Commande** : `python -m scripts.bronze_to_silver`
- **Rôle** : Lit Bronze → nettoie → normalise → détecte langue → écrit Silver

### gold-aggregator
- **Commande** : `python -m scripts.silver_to_gold`
- **Rôle** : Lit Silver → agrège tendances, topics, sources → écrit Gold

### warehouse-loader
- **Commande** : `python -m scripts.gold_to_warehouse`
- **Rôle** : Charge Gold JSON → tables PostgreSQL

### full-pipeline
- **Commande** : `python -m scripts.run_full_pipeline`
- **Rôle** : Exécute les 4 étapes en séquence (scrape → bronze → silver → gold → warehouse)

## Orchestration Airflow (3 services)

### airflow-init
- **Image** : Custom (`orchestration/Dockerfile`)
- **Rôle** : Initialise la base Airflow + crée l'utilisateur admin
- **Exécution** : une seule fois

### airflow-webserver
- **Port** : 8080
- **Rôle** : Interface web Airflow pour visualiser et gérer les DAGs

### airflow-scheduler
- **Rôle** : Exécute les DAGs selon leur schedule

### Dockerfile Airflow (`orchestration/Dockerfile`)
- Base : `apache/airflow:2.9.3-python3.11`
- Installe `requirements.txt` du projet
- Copie tout le code source dans `/opt/airflow/`
- Les DAGs sont montés en volume depuis `orchestration/dags/`

## Visualisation (1 service)

### metabase
- **Image** : `metabase/metabase:latest`
- **Port** : 3000
- **Rôle** : Dashboards de visualisation
- **Base interne** : `metabase` (PostgreSQL, pour les métadonnées Metabase)
- **Base de données à connecter** : `mediapulse` (via l'assistant de configuration)

## Monitoring (4 services)

### postgres-exporter
- **Image** : `prometheuscommunity/postgres-exporter:latest`
- **Rôle** : Expose les métriques PostgreSQL pour Prometheus
- **Métriques** : `pg_stat_activity_count`, `pg_database_size_bytes`, etc.

### kafka-exporter
- **Image** : `danielqsj/kafka-exporter:latest`
- **Rôle** : Expose les métriques Kafka pour Prometheus
- **Métriques** : `kafka_brokers`, `kafka_topic_partitions`, etc.

### prometheus
- **Image** : `prom/prometheus:latest`
- **Port** : 9090
- **Config** : `monitoring/prometheus.yml`
- **Targets scrappés** : prometheus, postgres, kafka, minio
- **Volume** : `prometheus-data`

### grafana
- **Image** : `grafana/grafana:latest`
- **Port** : 3001
- **Provisioning automatique** :
  - Datasource Prometheus : `monitoring/grafana/provisioning/datasources/prometheus.yml`
  - Dashboard Pipeline Health : `monitoring/grafana/dashboards/pipeline_health.json`
- **Volume** : `grafana-data`

## Réseau

Tous les services sont sur le réseau Docker `mediapulse` (bridge). Ils se joignent par leur nom de service (ex: `postgres`, `kafka`, `minio`).

## Volumes persistants

| Volume | Service | Données |
|--------|---------|---------|
| `zookeeper-data` | zookeeper | État du cluster |
| `kafka-data` | kafka | Messages et offsets |
| `minio-data` | minio | Objets Bronze/Silver/Gold |
| `postgres-data` | postgres | Tables du warehouse |
| `prometheus-data` | prometheus | Métriques historiques |
| `grafana-data` | grafana | Dashboards et préférences |
