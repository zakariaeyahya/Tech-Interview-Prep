# Préparation entretien — Data Scientist / ML Engineer

Deux pistes d'entraînement indépendantes.

## 🧩 [`algorithms/`](algorithms/) — Problem solving
Patterns algorithmiques type LeetCode (hash map, two pointers, sliding window, backtracking…),
avec solutions et tests.

```bash
python algorithms/run_all.py   # lance tous les tests
```

## 🤖 [`machine_learning/`](machine_learning/) — Machine learning
Notebooks **à compléter** (`# TODO`) reproduisant un pipeline d'entretien, avec corrigés séparés.

- [`classification_practice.ipynb`](machine_learning/classification_practice.ipynb) — scoring de défaut
- [`regression_practice.ipynb`](machine_learning/regression_practice.ipynb) — perte attendue
- Corrigés dans [`machine_learning/solutions/`](machine_learning/solutions/)

## Installation
```bash
pip install -r requirements.txt
```

## Contexte
Dataset synthétique de scoring de risque crédit (Coface-like) : voir
[`machine_learning/generate_dataset.py`](machine_learning/generate_dataset.py).
