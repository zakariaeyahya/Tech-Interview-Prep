"""
10. Backtracking (retour sur trace)
===================================
Explorer toutes les possibilites avec choix + annulation (backtrack).

Pattern :
def backtrack(chemin, options):
    if condition_arret:
        enregistrer(chemin)
        return
    for choix in options:
        appliquer(choix)
        backtrack(chemin, options)
        desfaire(choix)
"""

# ---------------------------------------------------------------------------
# Exemple 1 : Subsets (powerset)
# LeetCode 78
# ---------------------------------------------------------------------------
def subsets(nums: list[int]) -> list[list[int]]:
    result: list[list[int]] = []

    def backtrack(start: int, path: list[int]) -> None:
        result.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()

    backtrack(0, [])
    return result


# ---------------------------------------------------------------------------
# Exemple 2 : Permutations
# LeetCode 46
# ---------------------------------------------------------------------------
def permute(nums: list[int]) -> list[list[int]]:
    result: list[list[int]] = []

    def backtrack(path: list[int], remaining: list[int]) -> None:
        if not remaining:
            result.append(path[:])
            return
        for i, num in enumerate(remaining):
            backtrack(path + [num], remaining[:i] + remaining[i + 1 :])

    backtrack([], nums)
    return result


# ---------------------------------------------------------------------------
# Exemple 3 : Combination Sum
# LeetCode 39
# ---------------------------------------------------------------------------
def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    result: list[list[int]] = []
    candidates.sort()

    def backtrack(start: int, remaining: int, path: list[int]) -> None:
        if remaining == 0:
            result.append(path[:])
            return
        for i in range(start, len(candidates)):
            val = candidates[i]
            if val > remaining:
                break
            path.append(val)
            backtrack(i, remaining - val, path)
            path.pop()

    backtrack(0, target, [])
    return result


# ---------------------------------------------------------------------------
# Exemple 4 : N-Queens
# LeetCode 51
# ---------------------------------------------------------------------------
def solve_n_queens(n: int) -> list[list[str]]:
    result: list[list[str]] = []
    cols: set[int] = set()
    diag1: set[int] = set()
    diag2: set[int] = set()
    board = [-1] * n

    def backtrack(row: int) -> None:
        if row == n:
            result.append(["." * c + "Q" + "." * (n - c - 1) for c in board])
            return
        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            board[row] = col
            backtrack(row + 1)
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)

    backtrack(0)
    return result


# ---------------------------------------------------------------------------
# Exemple 5 : Generate Parentheses
# LeetCode 22
# ---------------------------------------------------------------------------
def generate_parenthesis(n: int) -> list[str]:
    result: list[str] = []

    def backtrack(current: str, open_count: int, close_count: int) -> None:
        if len(current) == 2 * n:
            result.append(current)
            return
        if open_count < n:
            backtrack(current + "(", open_count + 1, close_count)
        if close_count < open_count:
            backtrack(current + ")", open_count, close_count + 1)

    backtrack("", 0, 0)
    return result


# ---------------------------------------------------------------------------
# Exemple 6 : Word Search dans une grille
# LeetCode 79
# ---------------------------------------------------------------------------
def exist(board: list[list[str]], word: str) -> bool:
    rows, cols = len(board), len(board[0])

    def backtrack(r: int, c: int, index: int) -> bool:
        if index == len(word):
            return True
        if r < 0 or c < 0 or r >= rows or c >= cols or board[r][c] != word[index]:
            return False

        temp = board[r][c]
        board[r][c] = "#"
        found = (
            backtrack(r + 1, c, index + 1)
            or backtrack(r - 1, c, index + 1)
            or backtrack(r, c + 1, index + 1)
            or backtrack(r, c - 1, index + 1)
        )
        board[r][c] = temp
        return found

    for r in range(rows):
        for c in range(cols):
            if backtrack(r, c, 0):
                return True
    return False


def run_tests() -> None:
    assert subsets([1, 2, 3]) == [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]
    assert permute([1, 2, 3]) == [
        [1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]
    ]
    assert combination_sum([2, 3, 6, 7], 7) == [[2, 2, 3], [7]]
    assert len(solve_n_queens(4)) == 2
    assert generate_parenthesis(3) == ["((()))", "(()())", "(())()", "()(())", "()()()"]
    assert exist([["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]], "ABCCED") is True
    print("Tous les tests backtracking OK")


if __name__ == "__main__":
    run_tests()
