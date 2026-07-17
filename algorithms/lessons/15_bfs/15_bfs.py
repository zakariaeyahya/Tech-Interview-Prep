"""
15. BFS (parcours en largeur / Breadth-First Search)
====================================================
On explore niveau par niveau depuis une source, avec une file (queue).
Garantit le plus court chemin en nombre d'aretes dans un graphe non pondere.

Idee cle : file FIFO + ensemble des visites. Traiter tout un niveau
avant de passer au suivant (boucle sur len(queue)).
"""

from collections import deque
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ---------------------------------------------------------------------------
# Exemple 1 : Parcours par niveaux d'un arbre binaire
# LeetCode 102 | O(n)
# ---------------------------------------------------------------------------
def level_order(root: Optional[TreeNode]) -> list[list[int]]:
    if not root:
        return []
    result, queue = [], deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):            # tout le niveau courant
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level)
    return result


# ---------------------------------------------------------------------------
# Exemple 2 : Plus court chemin dans une grille (0 libre, 1 mur)
# LeetCode 1091 (variante) | O(n*m)
# ---------------------------------------------------------------------------
def shortest_path_grid(grid: list[list[int]]) -> int:
    if not grid or grid[0][0] == 1:
        return -1
    n, m = len(grid), len(grid[0])
    queue = deque([(0, 0, 1)])                 # (ligne, col, distance)
    seen = {(0, 0)}
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        r, c, dist = queue.popleft()
        if r == n - 1 and c == m - 1:
            return dist
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < m and grid[nr][nc] == 0 and (nr, nc) not in seen:
                seen.add((nr, nc))
                queue.append((nr, nc, dist + 1))
    return -1


# ---------------------------------------------------------------------------
# Exemple 3 : Nombre de niveaux (profondeur) d'un arbre
# LeetCode 104 | O(n)
# ---------------------------------------------------------------------------
def max_depth(root: Optional[TreeNode]) -> int:
    if not root:
        return 0
    depth, queue = 0, deque([root])
    while queue:
        depth += 1
        for _ in range(len(queue)):
            node = queue.popleft()
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    return depth


# ---------------------------------------------------------------------------
# Exemple 4 : Oranges pourries (BFS multi-source)
# LeetCode 994 | O(n*m)
# ---------------------------------------------------------------------------
def oranges_rotting(grid: list[list[int]]) -> int:
    n, m = len(grid), len(grid[0])
    queue = deque()
    fresh = 0
    for r in range(n):
        for c in range(m):
            if grid[r][c] == 2:
                queue.append((r, c))
            elif grid[r][c] == 1:
                fresh += 1

    minutes = 0
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while queue and fresh:
        minutes += 1
        for _ in range(len(queue)):
            r, c = queue.popleft()
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < m and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    queue.append((nr, nc))
    return minutes if fresh == 0 else -1


def run_tests() -> None:
    #        1
    #       / \
    #      2   3
    #     / \
    #    4   5
    root = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))
    assert level_order(root) == [[1], [2, 3], [4, 5]]
    assert max_depth(root) == 3
    assert level_order(None) == []

    grid = [[0, 0, 1], [1, 0, 0], [1, 1, 0]]
    assert shortest_path_grid(grid) == 5
    assert shortest_path_grid([[1, 0]]) == -1

    assert oranges_rotting([[2, 1, 1], [1, 1, 0], [0, 1, 1]]) == 4
    assert oranges_rotting([[2, 1, 1], [0, 1, 1], [1, 0, 1]]) == -1

    print("Tous les tests bfs OK")


if __name__ == "__main__":
    run_tests()
