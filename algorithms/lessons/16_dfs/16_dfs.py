"""
16. DFS (parcours en profondeur / Depth-First Search)
=====================================================
On explore aussi loin que possible avant de revenir en arriere.
Implementation par recursion (pile d'appels) ou pile explicite.

Idee cle : marquer le noeud visite, explorer recursivement chaque voisin.
Ideal pour : composantes connexes, chemins, structures arborescentes.
"""

from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ---------------------------------------------------------------------------
# Exemple 1 : Nombre d'iles (DFS sur grille)
# LeetCode 200 | O(n*m)
# ---------------------------------------------------------------------------
def num_islands(grid: list[list[str]]) -> int:
    if not grid:
        return 0
    n, m = len(grid), len(grid[0])

    def sink(r: int, c: int) -> None:
        if 0 <= r < n and 0 <= c < m and grid[r][c] == "1":
            grid[r][c] = "0"                   # marquer visite
            sink(r + 1, c)
            sink(r - 1, c)
            sink(r, c + 1)
            sink(r, c - 1)

    count = 0
    for r in range(n):
        for c in range(m):
            if grid[r][c] == "1":
                count += 1
                sink(r, c)
    return count


# ---------------------------------------------------------------------------
# Exemple 2 : Parcours prefixe (preorder) d'un arbre
# LeetCode 144 | O(n)
# ---------------------------------------------------------------------------
def preorder(root: Optional[TreeNode]) -> list[int]:
    result: list[int] = []

    def visit(node: Optional[TreeNode]) -> None:
        if not node:
            return
        result.append(node.val)                # racine
        visit(node.left)                       # gauche
        visit(node.right)                      # droite

    visit(root)
    return result


# ---------------------------------------------------------------------------
# Exemple 3 : Aire maximale d'une ile
# LeetCode 695 | O(n*m)
# ---------------------------------------------------------------------------
def max_area_of_island(grid: list[list[int]]) -> int:
    n, m = len(grid), len(grid[0])

    def area(r: int, c: int) -> int:
        if 0 <= r < n and 0 <= c < m and grid[r][c] == 1:
            grid[r][c] = 0
            return 1 + area(r + 1, c) + area(r - 1, c) + area(r, c + 1) + area(r, c - 1)
        return 0

    best = 0
    for r in range(n):
        for c in range(m):
            if grid[r][c] == 1:
                best = max(best, area(r, c))
    return best


# ---------------------------------------------------------------------------
# Exemple 4 : Composantes connexes d'un graphe (liste d'adjacence)
# O(V + E)
# ---------------------------------------------------------------------------
def count_components(n: int, edges: list[list[int]]) -> int:
    adj: dict[int, list[int]] = {i: [] for i in range(n)}
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)

    seen: set[int] = set()

    def dfs(node: int) -> None:
        seen.add(node)
        for nxt in adj[node]:
            if nxt not in seen:
                dfs(nxt)

    components = 0
    for node in range(n):
        if node not in seen:
            components += 1
            dfs(node)
    return components


def run_tests() -> None:
    grid = [
        ["1", "1", "0", "0"],
        ["1", "0", "0", "1"],
        ["0", "0", "1", "1"],
    ]
    assert num_islands(grid) == 2

    root = TreeNode(1, None, TreeNode(2, TreeNode(3)))
    assert preorder(root) == [1, 2, 3]

    assert max_area_of_island([[0, 1, 0], [1, 1, 0], [0, 0, 1]]) == 3

    assert count_components(5, [[0, 1], [1, 2], [3, 4]]) == 2
    assert count_components(4, []) == 4

    print("Tous les tests dfs OK")


if __name__ == "__main__":
    run_tests()
