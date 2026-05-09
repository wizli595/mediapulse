#!/bin/bash
# ============================================================
# MediaPulse — End-to-End Demo Script
# ============================================================
# Ce script lance une démonstration complète du pipeline :
#   1. Démarrage de l'infrastructure
#   2. Scraping des articles
#   3. Traitement Bronze → Silver → Gold
#   4. Chargement dans le Data Warehouse
#   5. Vérification des données
# ============================================================

set -e

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

step() {
    echo ""
    echo -e "${CYAN}============================================================${NC}"
    echo -e "${CYAN}  $1${NC}"
    echo -e "${CYAN}============================================================${NC}"
    echo ""
}

success() {
    echo -e "${GREEN}[OK] $1${NC}"
}

info() {
    echo -e "${YELLOW}[INFO] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
}

# -----------------------------------------------------------
# 0. Vérification des prérequis
# -----------------------------------------------------------
step "0. Vérification des prérequis"

if ! command -v docker &> /dev/null; then
    error "Docker n'est pas installé."
    exit 1
fi
success "Docker trouvé"

if ! docker compose version &> /dev/null; then
    error "Docker Compose n'est pas installé."
    exit 1
fi
success "Docker Compose trouvé"

# -----------------------------------------------------------
# 1. Démarrage de l'infrastructure
# -----------------------------------------------------------
step "1. Démarrage de l'infrastructure (Kafka, MinIO, PostgreSQL)"

docker compose up -d zookeeper kafka minio postgres
info "Attente que les services soient prêts..."
sleep 10

docker compose run --rm init-buckets
success "Buckets MinIO créés (bronze, silver, gold)"

# -----------------------------------------------------------
# 2. Scraping des articles
# -----------------------------------------------------------
step "2. Scraping des articles de presse"

info "Lancement du batch scraper..."
docker compose run --rm batch-scraper
success "Articles récupérés et stockés dans Bronze (MinIO)"

# -----------------------------------------------------------
# 3. Traitement Bronze → Silver
# -----------------------------------------------------------
step "3. Traitement Bronze → Silver (nettoyage, normalisation, déduplication)"

docker compose run --rm bronze-to-silver
success "Données nettoyées et stockées dans Silver"

# -----------------------------------------------------------
# 4. Traitement Silver → Gold
# -----------------------------------------------------------
step "4. Traitement Silver → Gold (agrégation, tendances, topics)"

docker compose run --rm gold-aggregator
success "Données agrégées et stockées dans Gold"

# -----------------------------------------------------------
# 5. Chargement dans le Data Warehouse
# -----------------------------------------------------------
step "5. Chargement Gold → PostgreSQL (Data Warehouse)"

docker compose run --rm warehouse-loader
success "Données chargées dans PostgreSQL"

# -----------------------------------------------------------
# 6. Vérification des données
# -----------------------------------------------------------
step "6. Vérification des données dans le Data Warehouse"

echo ""
info "Articles par source :"
docker exec mediapulse-postgres psql -U mediapulse -d mediapulse \
    -c "SELECT source, COUNT(*) as nb_articles FROM articles GROUP BY source ORDER BY nb_articles DESC;"

echo ""
info "Articles par langue :"
docker exec mediapulse-postgres psql -U mediapulse -d mediapulse \
    -c "SELECT language, COUNT(*) as nb_articles FROM articles GROUP BY language ORDER BY nb_articles DESC;"

echo ""
info "Total des articles :"
docker exec mediapulse-postgres psql -U mediapulse -d mediapulse \
    -c "SELECT COUNT(*) as total_articles FROM articles;"

# -----------------------------------------------------------
# 7. Démarrage des services web
# -----------------------------------------------------------
step "7. Démarrage des services web"

docker compose up -d airflow-init
sleep 5
docker compose up -d airflow-webserver airflow-scheduler
docker compose up -d dashboard-api dashboard-ui
docker compose up -d metabase
docker compose up -d prometheus grafana

success "Tous les services sont démarrés"

echo ""
echo -e "${GREEN}============================================================${NC}"
echo -e "${GREEN}  DEMO TERMINEE${NC}"
echo -e "${GREEN}============================================================${NC}"
echo ""
echo -e "  Dashboard      : ${CYAN}http://localhost:3000${NC}"
echo -e "  Dashboard API  : ${CYAN}http://localhost:8000${NC}"
echo -e "  Airflow        : ${CYAN}http://localhost:8080${NC}  (admin/admin)"
echo -e "  Metabase       : ${CYAN}http://localhost:3002${NC}"
echo -e "  MinIO Console  : ${CYAN}http://localhost:9001${NC}  (mediapulse/changeme123)"
echo -e "  Grafana        : ${CYAN}http://localhost:3001${NC}  (admin/admin)"
echo -e "  Prometheus     : ${CYAN}http://localhost:9090${NC}"
echo ""
