# Machine Learning — Entraînement entretien

## Comment t'entraîner

1. Installe les dépendances : `pip install -r ../requirements.txt`
2. Ouvre un notebook de pratique et remplis les cellules `# TODO` dans l'ordre.
3. **Sans regarder le corrigé.** Le résultat attendu est indiqué en commentaire.
4. Une fois fini, vérifie ton raisonnement avec le script de `solutions/`.

## Contenu

| Fichier | Cible | Sujet |
|---|---|---|
| [`classification_practice.ipynb`](classification_practice.ipynb) | `defaulted` | LogisticRegression → RandomForest → XGBoost, déséquilibre, seuil métier |
| [`regression_practice.ipynb`](regression_practice.ipynb) | `expected_loss` | LinearRegression → polynomiale → XGBRegressor, résidus, overfitting |
| [`machine_learning_test.ipynb`](machine_learning_test.ipynb) | — | Questions théoriques ML (45 min) |
| [`python_test.ipynb`](python_test.ipynb) | — | Test Python / pandas |
| [`solutions/`](solutions/) | — | **Corrigés complets** (à consulter après) |

## Lancer les corrigés
Depuis ce dossier (`machine_learning/`) :
```bash
python solutions/classification_xgboost.py
python solutions/regression_xgboost.py
```
Les graphiques sont écrits dans [`outputs/`](outputs/). Le dataset est dans
[`data/credit_risk.csv`](data/) — régénérable via `python generate_dataset.py`.

## Données
| Colonne | Type | Description |
|---|---|---|
| `country`, `sector` | catégoriel | pays / secteur de l'entreprise |
| `revenue`, `debt_ratio`, `days_late`, `num_employees`, `credit_score`, `years_in_business` | numérique | features explicatives |
| `defaulted` | binaire | **cible classification** (1 = défaut) |
| `expected_loss` | continu | **cible régression** (perte attendue) |
