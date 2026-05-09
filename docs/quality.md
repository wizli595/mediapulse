# Qualité des données

## Principe

Chaque article passe par un ensemble de checks **avant** d'être écrit dans le Data Lake. Chaque check valide **une seule règle** et retourne un verdict `PASS` ou `FAIL`.

## Dimensions de qualité

| Dimension | Description | Checks associés |
|-----------|-------------|----------------|
| **Complétude** | Tous les champs obligatoires sont présents | `title_present`, `date_present` |
| **Cohérence** | Les données sont logiquement cohérentes | `url_valid` |
| **Validité** | Les valeurs respectent les contraintes métier | `content_length` |

## Checks implémentés

### title_present
- **Dimension** : Complétude
- **Règle** : Le titre ne doit pas être vide
- **Fichier** : `quality/checks/title_present.py`

### date_present
- **Dimension** : Complétude
- **Règle** : La date de publication ne doit pas être nulle
- **Fichier** : `quality/checks/date_present.py`

### content_length
- **Dimension** : Validité
- **Règle** : Le contenu doit faire au moins 50 caractères
- **Fichier** : `quality/checks/content_length.py`

### url_valid
- **Dimension** : Cohérence
- **Règle** : L'URL doit avoir un schéma http/https et un host valide
- **Fichier** : `quality/checks/url_valid.py`

## Architecture

```python
# Chaque check implémente AbstractCheck
class AbstractCheck(ABC):
    @property
    def name(self) -> str: ...
    @property
    def dimension(self) -> Dimension: ...
    def run(self, article: Article) -> CheckResult: ...

# Le validateur exécute tous les checks
def validate_article(article: Article) -> ValidationReport:
    # Retourne un rapport avec passed/failures
```

## Rapport de validation

```python
report = validate_article(article)

report.passed      # True si tous les checks passent
report.failures    # Liste des CheckResult échoués
report.article_id  # ID de l'article validé
```

## Ajouter un nouveau check

1. Créer `quality/checks/mon_check.py` :
```python
class MonCheck(AbstractCheck):
    @property
    def name(self) -> str:
        return "mon_check"

    @property
    def dimension(self) -> Dimension:
        return Dimension.VALIDITY

    def run(self, article: Article) -> CheckResult:
        if condition:
            return CheckResult(self.name, self.dimension, Status.PASS, "OK")
        return CheckResult(self.name, self.dimension, Status.FAIL, "Raison")
```

2. Ajouter dans `quality/validator.py` :
```python
_ALL_CHECKS = [
    ...,
    MonCheck(),
]
```

Rien d'autre à modifier.
