"""
17. Topological Sort (tri topologique)
======================================
Ordonne les sommets d'un graphe oriente acyclique (DAG) de sorte que
chaque arete u -> v place u avant v. Sert a ordonnancer des taches avec
dependances (compilation, cursus, build system).

Algorithme de Kahn (BFS) : on part des sommets sans dependance
(in-degree 0), on les retire, on decremente les voisins. Si tous les
sommets sont sortis, pas de cycle ; sinon il y a un cycle.
"""

from collections import deque


# ---------------------------------------------------------------------------
# Exemple 1 : Tri topologique (Kahn) -> ordre valide ou [] si cycle
# O(V + E)
# ---------------------------------------------------------------------------
def topological_order(n: int, edges: list[list[int]]) -> list[int]:
    adj: dict[int, list[int]] = {i: [] for i in range(n)}
    indeg = [0] * n
    for u, v in edges:                         # u -> v (u avant v)
        adj[u].append(v)
        indeg[v] += 1

    queue = deque(i for i in range(n) if indeg[i] == 0)
    order: list[int] = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for nxt in adj[node]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                queue.append(nxt)

    return order if len(order) == n else []    # [] => cycle detecte


# ---------------------------------------------------------------------------
# Exemple 2 : Course Schedule - peut-on tout terminer ?
# LeetCode 207 | O(V + E)
# ---------------------------------------------------------------------------
def can_finish(num_courses: int, prerequisites: list[list[int]]) -> bool:
    # prerequisites[i] = [a, b] : b doit preceder a  (b -> a)
    edges = [[b, a] for a, b in prerequisites]
    return len(topological_order(num_courses, edges)) == num_courses


# ---------------------------------------------------------------------------
# Exemple 3 : Course Schedule II - un ordre valide de cours
# LeetCode 210 | O(V + E)
# ---------------------------------------------------------------------------
def find_order(num_courses: int, prerequisites: list[list[int]]) -> list[int]:
    edges = [[b, a] for a, b in prerequisites]
    return topological_order(num_courses, edges)


def run_tests() -> None:
    order = topological_order(6, [[5, 2], [5, 0], [4, 0], [4, 1], [2, 3], [3, 1]])
    # Verifier que c'est un ordre topologique valide
    assert len(order) == 6
    pos = {node: i for i, node in enumerate(order)}
    for u, v in [[5, 2], [5, 0], [4, 0], [4, 1], [2, 3], [3, 1]]:
        assert pos[u] < pos[v]

    # Cycle -> pas d'ordre
    assert topological_order(2, [[0, 1], [1, 0]]) == []

    assert can_finish(2, [[1, 0]]) is True
    assert can_finish(2, [[1, 0], [0, 1]]) is False

    result = find_order(4, [[1, 0], [2, 0], [3, 1], [3, 2]])
    assert len(result) == 4 and result[0] == 0 and result[-1] == 3

    print("Tous les tests topological_sort OK")


if __name__ == "__main__":
    run_tests()
