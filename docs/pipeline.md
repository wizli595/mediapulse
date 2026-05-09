# Pipeline de données

## Vue d'ensemble

Le pipeline MediaPulse transforme des pages HTML en données analytiques exploitables via 4 étapes séquentielles.

```
Scraping → Bronze → Silver → Gold → Warehouse → Dashboards
```

## Étape 1 : Scraping → Bronze

**Script** : `scripts/batch_scrape.py`
**Docker** : `docker compose run --rm batch-scraper`

### Fonctionnement
1. Les 8 spiders sont exécutés (`scrapers/runner.py`)
2. Chaque spider :
   - Récupère les URLs d'articles depuis la page d'accueil
   - Parse chaque article (titre, auteur, date, contenu, catégorie)
3. Chaque article est validé (`quality/validator.py`)
4. Les articles valides sont :
   - Écrits dans MinIO Bronze : `bronze/{source}/{date}/{id}.json`
   - Publiés sur le topic Kafka `raw-articles`

### Données collectées par article

| Champ | Type | Obligatoire |
|-------|------|-------------|
| title | str | oui |
| content | str | oui |
| source | str | oui |
| url | str | oui |
| published_at | datetime | oui |
| author | str | non |
| category | str | non |
| language | str | non (détecté en Silver) |

## Étape 2 : Bronze → Silver

**Script** : `scripts/bronze_to_silver.py`
**Docker** : `docker compose run --rm bronze-to-silver`

### Transformations appliquées (dans l'ordre)

| Transformation | Fichier | Description |
|----------------|---------|-------------|
| Déduplication | `deduplicator.py` | Vérifie si l'article existe déjà dans Silver |
| Nettoyage HTML | `html_cleaner.py` | Supprime les balises HTML et décode les entités |
| Normalisation | `text_normalizer.py` | Unicode NFKC, supprime les caractères de contrôle, collapse les espaces |
| Détection langue | `language_detector.py` | Retourne le code ISO 639-1 (ar, en, fr...) |

### Résultat
Article nettoyé écrit dans MinIO Silver : `silver/{source}/{date}/{id}.json`

## Étape 3 : Silver → Gold

**Script** : `scripts/silver_to_gold.py`
**Docker** : `docker compose run --rm gold-aggregator`

### Agrégations produites

| Fichier | Contenu | Fonction |
|---------|---------|----------|
| `gold/trends.json` | Articles par date + source + catégorie | `compute_trends()` |
| `gold/topics.json` | Top 50 mots-clés par fréquence | `extract_topics()` |
| `gold/sources.json` | Total articles par source | `count_by_source()` |

### Extraction de mots-clés
- Mots de 3+ caractères extraits du contenu
- Stopwords filtrés (anglais + arabe)
- Classés par fréquence décroissante

## Étape 4 : Gold → Warehouse

**Script** : `scripts/gold_to_warehouse.py`
**Docker** : `docker compose run --rm warehouse-loader`

### Tables PostgreSQL alimentées

| Table | Source | Stratégie |
|-------|--------|-----------|
| `articles` | Silver JSON | Upsert (ON CONFLICT) |
| `trends` | Gold trends.json | Upsert par (date, source, category) |
| `topics` | Gold topics.json | Full replace (DELETE + INSERT) |

## Pipeline complet

**Script** : `scripts/run_full_pipeline.py`
**Docker** : `docker compose run --rm full-pipeline`

Exécute les 4 étapes en séquence.

## Streaming (temps réel)

En parallèle du batch, le `stream-consumer` tourne en permanence :
- Lit les messages du topic Kafka `raw-articles`
- Applique le pipeline Silver sur chaque article reçu
- Écrit le résultat dans MinIO Silver

```bash
# Le consumer tourne automatiquement avec docker compose up
docker compose logs -f stream-consumer
```

## Orchestration Airflow

Les 4 DAGs Airflow automatisent le pipeline :

| DAG | Schedule | Étape |
|-----|----------|-------|
| `batch_scrape` | Toutes les heures | Scraping → Bronze → Kafka |
| `bronze_to_silver` | Toutes les heures | Bronze → Silver |
| `silver_to_gold` | Toutes les 2 heures | Silver → Gold |
| `gold_to_warehouse` | Toutes les 2 heures | Gold → PostgreSQL |

Activer les DAGs dans l'UI Airflow : http://localhost:8080
