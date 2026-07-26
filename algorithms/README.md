# Algorithms — Problem solving

Patterns algorithmiques classiques (type entretien / LeetCode), avec solutions commentées
et tests intégrés (`run_tests()` dans chaque fichier).

## Structure du dossier

```
algorithms/
├── lessons/      un sous-dossier par pattern (.py + .ipynb ensemble)
├── courses/      cours LaTeX / PDF (cours.*, python_cours.*)
├── slides/       présentations (.pptx, .js)
├── run_all.py    lance tous les tests des lessons/
└── README.md
```

## Patterns (dans `lessons/`)

| Dossier | Pattern | Exemples |
|---|---|---|
| [`01_hash_map`](lessons/01_hash_map) | Hash map / dictionnaire | Two Sum, anagrammes, fréquences |
| [`02_hash_set`](lessons/02_hash_set) | Hash set | doublons, présence O(1) |
| [`03_two_pointers`](lessons/03_two_pointers) | Two pointers | paires triées, palindrome |
| [`04_sliding_window`](lessons/04_sliding_window) | Sliding window | sous-tableau / sous-chaîne optimal |
| [`05_prefix_sum`](lessons/05_prefix_sum) | Prefix sum | sommes de sous-tableaux |
| [`06_sorting`](lessons/06_sorting) | Tri | tris et variantes |
| [`07_binary_search`](lessons/07_binary_search) | Recherche binaire | recherche en O(log n) |
| [`08_stack`](lessons/08_stack) | Pile | parenthèses, évaluation |
| [`09_monotonic_stack`](lessons/09_monotonic_stack) | Pile monotone | next greater element |
| [`10_backtracking`](lessons/10_backtracking) | Backtracking | permutations, combinaisons |
| [`11_linked_list`](lessons/11_linked_list) | Liste chaînée | inversion, cycle |
| [`12_fast_slow_pointers`](lessons/12_fast_slow_pointers) | Fast & slow (Floyd) | cycle, milieu, happy number |
| [`13_merge_intervals`](lessons/13_merge_intervals) | Merge intervals | fusion, insertion, salles de réunion |
| [`14_cyclic_sort`](lessons/14_cyclic_sort) | Cyclic sort | nombre manquant / dupliqué |
| [`15_bfs`](lessons/15_bfs) | BFS (largeur) | niveaux d'arbre, plus court chemin |
| [`16_dfs`](lessons/16_dfs) | DFS (profondeur) | îles, composantes connexes |
| [`17_topological_sort`](lessons/17_topological_sort) | Tri topologique (Kahn) | ordonnancement, prérequis |
| [`18_union_find`](lessons/18_union_find) | Union-Find / DSU | composantes, cycle non orienté |
| [`19_dynamic_programming`](lessons/19_dynamic_programming) | Programmation dynamique | coin change, LIS, sac à dos |
| [`20_greedy`](lessons/20_greedy) | Glouton | jump game, intervalles |
| [`21_bit_manipulation`](lessons/21_bit_manipulation) | Manipulation de bits | XOR, comptage de bits |

## Deux formats disponibles

Chaque pattern existe en **deux versions** dans son dossier :

- **`.py`** — script exécutable en ligne de commande, testé par `run_all.py`.
- **`.ipynb`** — notebook Jupyter : une cellule markdown d'explication, une cellule
  de code par fonction, puis une cellule de test à exécuter. Idéal pour réviser pas à pas.

En plus :

| Dossier | Rôle |
|---|---|
| [`00_revision_python`](lessons/00_revision_python) | Révision des **fondamentaux Python** (types, structures, boucles, fonctions, classes, exceptions, comprehensions, générateurs, pièges) — interactif, avec exercices |

## Lancer tous les tests
```bash
python run_all.py          # parcourt lessons/**/*.py
```
Pour les notebooks, ouvre-les dans Jupyter / VS Code et exécute « Run All » :
la dernière cellule appelle `run_tests()` et affiche `OK` si tout passe.

## S'entraîner
- **En script** : lis l'énoncé en haut de chaque `.py`, masque la solution,
  ré-implémente la fonction, puis exécute le fichier
  (`python lessons/01_hash_map/01_hash_map.py`).
- **En notebook** : ouvre le `.ipynb`, lis l'explication, réécris chaque fonction
  dans sa cellule, puis lance la cellule de test juste en dessous.
