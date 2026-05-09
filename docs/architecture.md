# Architecture

## Vue d'ensemble

MediaPulse suit une **architecture Lambda** combinant traitement batch et streaming, organisée en couches indépendantes.

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│  SCRAPING   │────►│  INGESTION   │────►│  DATA LAKE   │
│  (Scrapy)   │     │  (Kafka)     │     │  (MinIO)     │
└─────────────┘     └──────────────┘     └──────┬───────┘
                                                │
                                    ┌───────────┼───────────┐
                                    │           │           │
                               ┌────▼───┐ ┌────▼───┐ ┌────▼───┐
                               │ BRONZE │ │ SILVER │ │  GOLD  │
                               │ (brut) │ │(clean) │ │(agrégé)│
                               └────────┘ └────────┘ └────┬───┘
                                                          │
                                                ┌─────────▼─────────┐
                                                │   DATA WAREHOUSE  │
                                                │   (PostgreSQL)    │
                                                └─────────┬─────────┘
                                                          │
                                                ┌─────────▼─────────┐
                                                │   VISUALISATION   │
                                                │   (Metabase)      │
                                                └───────────────────┘
```

## Architecture Médaillon

### Bronze (Données brutes)
- Articles JSON tels que scrappés
- Stockés dans MinIO : `bronze/{source}/{YYYY}/{MM}/{DD}/{article_id}.json`
- Aucune transformation appliquée
- Sert d'historique complet et immuable

### Silver (Données nettoyées)
- HTML supprimé (`strip_html`)
- Texte normalisé (unicode, espaces)
- Langue détectée (ISO 639-1)
- Articles dédupliqués par `article_id`
- Stockés dans MinIO : `silver/{source}/{YYYY}/{MM}/{DD}/{article_id}.json`

### Gold (Données agrégées)
- `trends.json` : nombre d'articles par date + source + catégorie
- `topics.json` : top 50 mots-clés par fréquence
- `sources.json` : total articles par source

## Principes Clean Code

### Single Responsibility (SRP)
Chaque fonction fait UNE chose. Chaque classe a UNE raison de changer.

Exemples :
- Un spider parse du HTML. Il ne sauvegarde pas, ne publie pas.
- Un publisher envoie à Kafka. Il ne scrappe pas.
- Un check de qualité valide une règle. Il ne corrige pas.

### Dependency Inversion (DIP)
Chaque couche définit une classe abstraite. Les implémentations sont interchangeables.

```python
AbstractSpider    → HespressSpider, BBCSpider, ...
AbstractPublisher → KafkaPublisher, FilePublisher
AbstractStorage   → MinIOStorage, LocalStorage
AbstractCheck     → TitlePresentCheck, DatePresentCheck, ...
```

### Open/Closed (OCP)
- Ajouter une source = ajouter un fichier spider + une ligne dans le registre
- Ajouter un check = ajouter un fichier check + une ligne dans le validateur

### Flux de dépendances

```
scrapers → ingestion → storage → processing → warehouse → visualization
    │          │           │           │            │
    └──────────┴───────────┴───────────┴────────────┘
                           │
                     shared/models
                     shared/config
                     shared/exceptions
```

Chaque couche dépend uniquement de `shared/` et de la couche précédente. Pas de dépendances circulaires.

## Choix techniques

| Choix | Justification |
|-------|---------------|
| **MinIO** plutôt que HDFS | Léger, S3-compatible, parfait pour Docker |
| **Kafka** pour le streaming | Standard industriel, découplage producteur/consommateur |
| **PostgreSQL** pour le DWH | SQL natif, fiable, connectors Metabase natifs |
| **Metabase** pour la visualisation | Setup Docker simple, requêtes SQL natives |
| **Airflow** pour l'orchestration | Standard pour les pipelines data, UI web |
| **Prometheus + Grafana** pour le monitoring | Stack standard, métriques temps réel |
| **Python** partout | Cohérence, écosystème riche pour le scraping et le traitement |
