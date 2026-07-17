"""
18. Union-Find / DSU (Disjoint Set Union)
=========================================
Structure qui gere des ensembles disjoints avec deux operations quasi
constantes : find(x) (representant de l'ensemble) et union(a, b) (fusion).

Deux optimisations essentielles :
  - path compression : find aplati l'arbre au passage.
  - union by rank/size : on accroche le petit arbre sous le grand.
Complexite amortie ~ O(alpha(n)), pratiquement O(1).

Ideal pour : composantes connexes dynamiques, detection de cycle dans un
graphe non oriente, Kruskal (MST), regroupement.
"""


class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.count = n                          # nb d'ensembles disjoints

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]  # path compression
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False                        # deja dans le meme ensemble
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra                    # union by rank
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        self.count -= 1
        return True

    def connected(self, a: int, b: int) -> bool:
        return self.find(a) == self.find(b)


# ---------------------------------------------------------------------------
# Exemple 1 : Nombre de provinces (composantes connexes)
# LeetCode 547 | O(n^2 * alpha)
# ---------------------------------------------------------------------------
def find_circle_num(is_connected: list[list[int]]) -> int:
    n = len(is_connected)
    uf = UnionFind(n)
    for i in range(n):
        for j in range(i + 1, n):
            if is_connected[i][j] == 1:
                uf.union(i, j)
    return uf.count


# ---------------------------------------------------------------------------
# Exemple 2 : Detecter un cycle dans un graphe non oriente
# LeetCode 684 (variante) | O(E * alpha)
# ---------------------------------------------------------------------------
def has_cycle_undirected(n: int, edges: list[list[int]]) -> bool:
    uf = UnionFind(n)
    for a, b in edges:
        if not uf.union(a, b):                  # deja connectes -> cycle
            return True
    return False


# ---------------------------------------------------------------------------
# Exemple 3 : Redundant Connection (arete qui cree le cycle)
# LeetCode 684 | O(E * alpha)
# ---------------------------------------------------------------------------
def find_redundant_connection(edges: list[list[int]]) -> list[int]:
    uf = UnionFind(len(edges) + 1)              # sommets 1..n
    for a, b in edges:
        if not uf.union(a, b):
            return [a, b]
    return []


def run_tests() -> None:
    uf = UnionFind(5)
    assert uf.union(0, 1) is True
    assert uf.union(1, 2) is True
    assert uf.union(0, 2) is False              # deja connectes
    assert uf.connected(0, 2) is True
    assert uf.connected(0, 3) is False
    assert uf.count == 3                        # {0,1,2}, {3}, {4}

    assert find_circle_num([[1, 1, 0], [1, 1, 0], [0, 0, 1]]) == 2
    assert find_circle_num([[1, 0, 0], [0, 1, 0], [0, 0, 1]]) == 3

    assert has_cycle_undirected(3, [[0, 1], [1, 2], [2, 0]]) is True
    assert has_cycle_undirected(3, [[0, 1], [1, 2]]) is False

    assert find_redundant_connection([[1, 2], [1, 3], [2, 3]]) == [2, 3]

    print("Tous les tests union_find OK")


if __name__ == "__main__":
    run_tests()
