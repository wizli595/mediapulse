# Gouvernance des données

## Catalogue de données

Le fichier `governance/catalog.yml` documente l'ensemble du patrimoine de données :

### Sources enregistrées
8 sources d'actualité (4 marocaines, 4 internationales) avec URL, langue et méthode de collecte.

### Couches du Data Lake

| Couche | Bucket MinIO | Format | Clé |
|--------|-------------|--------|-----|
| Bronze | `bronze` | JSON brut | `{source}/{YYYY}/{MM}/{DD}/{article_id}.json` |
| Silver | `silver` | JSON nettoyé | `{source}/{YYYY}/{MM}/{DD}/{article_id}.json` |
| Gold | `gold` | JSON agrégé | `trends.json`, `topics.json`, `sources.json` |

### Tables du Data Warehouse

| Table | Description | Clé primaire | Rafraîchissement |
|-------|-------------|-------------|-----------------|
| `articles` | Tous les articles nettoyés | `article_id` | Upsert continu |
| `trends` | Articles par date/source/catégorie | `(date, source, category)` | Upsert toutes les 2h |
| `topics` | Top 50 mots-clés | `id` | Full replace toutes les 2h |
| `source_counts` | Total par source | `source` | Full replace toutes les 2h |

## Lignage des données

Le flux complet de transformation est documenté en 7 étapes :

```
1. Sites web (HTML)
   │  outil: Scrapy spiders
   ▼
2. Article objects (Python)
   │  outil: KafkaPublisher
   ▼
3. Kafka topic raw-articles
   │  outil: raw_writer.py
   ▼
4. MinIO Bronze (JSON brut)
   │  outil: silver/pipeline.py
   ▼
5. MinIO Silver (JSON nettoyé)
   │  outil: gold/pipeline.py
   ▼
6. MinIO Gold (JSON agrégé)
   │  outil: warehouse/repositories
   ▼
7. PostgreSQL (tables analytiques)
   │  outil: Metabase
   ▼
8. Dashboards
```

## Traçabilité

### article_id
Chaque article possède un identifiant déterministe calculé à partir de `sha256(source + url)`. Cet ID est :
- Stable entre les exécutions (même article = même ID)
- Utilisé pour la déduplication en Silver
- Utilisé comme clé primaire dans PostgreSQL
- Utilisé comme clé Kafka

### scraped_at
Chaque article porte un timestamp `scraped_at` qui enregistre quand il a été collecté, distinct de `published_at` (date de publication par le média).

### Organisation par date
Les objets dans MinIO sont organisés par date de publication : `{source}/{YYYY}/{MM}/{DD}/{id}.json`, facilitant les requêtes par période.

## Règles de qualité

Voir [quality.md](quality.md) pour les 4 checks appliqués à chaque article avant ingestion.

## Rétention

| Couche | Rétention |
|--------|-----------|
| Bronze | Indéfinie (historique complet) |
| Silver | Indéfinie |
| Gold | Écrasé à chaque agrégation |
| Warehouse | Indéfinie (upsert) |
