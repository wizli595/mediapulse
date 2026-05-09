# Guide d'installation

## Prérequis

- **Docker** 24+ avec Docker Compose v2
- **Git**
- 4 Go de RAM minimum (recommandé : 8 Go)
- Ports libres : 3000, 3001, 5432, 8080, 9000, 9001, 9090, 9092

## Installation

### 1. Cloner le projet

```bash
git clone https://github.com/wizli595/mediapulse.git
cd mediapulse
```

### 2. Configurer l'environnement

```bash
cp .env.example .env
```

Les valeurs par défaut fonctionnent directement. Modifier `.env` si nécessaire.

### 3. Lancer la plateforme

```bash
docker compose up -d --build
```

Premier lancement : ~5 minutes (téléchargement des images Docker).

### 4. Vérifier que tout fonctionne

```bash
docker compose ps
```

Tous les services doivent être `Up` ou `Healthy`.

### 5. Lancer le pipeline

```bash
docker compose run --rm full-pipeline
```

## Configuration des interfaces

### Airflow (http://localhost:8080)
- Login : `admin` / `admin`
- Les 4 DAGs sont visibles : `batch_scrape`, `bronze_to_silver`, `silver_to_gold`, `gold_to_warehouse`
- Activer les DAGs pour le scraping automatique

### Metabase (http://localhost:3000)
1. Compléter l'assistant de configuration
2. Ajouter une connexion base de données :
   - Type : **PostgreSQL**
   - Host : `postgres`
   - Port : `5432`
   - Database : `mediapulse`
   - Username : `mediapulse`
   - Password : `changeme123`
3. Créer des questions avec les requêtes de `visualization/metabase_queries.sql`

### MinIO Console (http://localhost:9001)
- Login : `mediapulse` / `changeme123`
- 3 buckets visibles : `bronze`, `silver`, `gold`

### Grafana (http://localhost:3001)
- Login : `admin` / `admin`
- Dashboard "Pipeline Health" auto-provisionné
- Datasource Prometheus configuré automatiquement

### Prometheus (http://localhost:9090)
- Pas d'authentification
- Vérifier les targets : Status → Targets

## Arrêter la plateforme

```bash
docker compose down        # Arrêter (données conservées)
docker compose down -v     # Arrêter + supprimer les volumes (reset complet)
```

## Développement local (sans Docker)

```bash
python -m venv venv
source venv/Scripts/activate   # Windows
source venv/bin/activate       # Linux/Mac
pip install -r requirements-dev.txt
PYTHONPATH=. pytest tests/ -v
```

## Problèmes courants

| Problème | Solution |
|----------|----------|
| Port déjà utilisé | Modifier les ports dans `docker-compose.yml` |
| Airflow ne démarre pas | Vérifier les logs : `docker compose logs airflow-init` |
| Metabase ne se connecte pas à la DB | Host = `postgres` (pas `localhost`) |
| MinIO healthcheck échoue | Attendre 30s, le service met du temps à démarrer |
