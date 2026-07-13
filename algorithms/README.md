# Algorithms — Problem solving

Patterns algorithmiques classiques (type entretien / LeetCode), avec solutions commentées
et tests intégrés (`run_tests()` dans chaque fichier).

| Fichier | Pattern | Exemples |
|---|---|---|
| [`01_hash_map.py`](01_hash_map.py) | Hash map / dictionnaire | Two Sum, anagrammes, fréquences |
| [`02_hash_set.py`](02_hash_set.py) | Hash set | doublons, présence O(1) |
| [`03_two_pointers.py`](03_two_pointers.py) | Two pointers | paires triées, palindrome |
| [`04_sliding_window.py`](04_sliding_window.py) | Sliding window | sous-tableau / sous-chaîne optimal |
| [`05_prefix_sum.py`](05_prefix_sum.py) | Prefix sum | sommes de sous-tableaux |
| [`06_sorting.py`](06_sorting.py) | Tri | tris et variantes |
| [`07_binary_search.py`](07_binary_search.py) | Recherche binaire | recherche en O(log n) |
| [`08_stack.py`](08_stack.py) | Pile | parenthèses, évaluation |
| [`09_monotonic_stack.py`](09_monotonic_stack.py) | Pile monotone | next greater element |
| [`10_backtracking.py`](10_backtracking.py) | Backtracking | permutations, combinaisons |
| [`11_linked_list.py`](11_linked_list.py) | Liste chaînée | inversion, cycle |
| [`12_fast_slow_pointers.py`](12_fast_slow_pointers.py) | Fast & slow (Floyd) | cycle, milieu, happy number |
| [`13_merge_intervals.py`](13_merge_intervals.py) | Merge intervals | fusion, insertion, salles de réunion |
| [`14_cyclic_sort.py`](14_cyclic_sort.py) | Cyclic sort | nombre manquant / dupliqué |
| [`15_bfs.py`](15_bfs.py) | BFS (largeur) | niveaux d'arbre, plus court chemin |
| [`16_dfs.py`](16_dfs.py) | DFS (profondeur) | îles, composantes connexes |
| [`17_topological_sort.py`](17_topological_sort.py) | Tri topologique (Kahn) | ordonnancement, prérequis |
| [`18_union_find.py`](18_union_find.py) | Union-Find / DSU | composantes, cycle non orienté |
| [`19_dynamic_programming.py`](19_dynamic_programming.py) | Programmation dynamique | coin change, LIS, sac à dos |
| [`20_greedy.py`](20_greedy.py) | Glouton | jump game, intervalles |
| [`21_bit_manipulation.py`](21_bit_manipulation.py) | Manipulation de bits | XOR, comptage de bits |

## Lancer tous les tests
```bash
python run_all.py
```

## S'entraîner
Lis l'énoncé en haut de chaque fichier, masque la solution, ré-implémente la fonction,
puis exécute le fichier pour valider (`python 01_hash_map.py`).
