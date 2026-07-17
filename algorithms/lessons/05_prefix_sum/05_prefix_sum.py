"""
5. Prefix Sum (somme prefixee)
==============================
prefix[i] = somme de nums[0..i-1]
Permet des requetes de somme sur un intervalle en O(1).

Formule : sum(i, j) = prefix[j+1] - prefix[i]
"""

from itertools import accumulate


# ---------------------------------------------------------------------------
# Exemple 1 : Construire le prefix sum
# ---------------------------------------------------------------------------
def build_prefix(nums: list[int]) -> list[int]:
    prefix = [0]
    for num in nums:
        prefix.append(prefix[-1] + num)
    return prefix


def range_sum(prefix: list[int], left: int, right: int) -> int:
    """Somme de nums[left..right] inclusive."""
    return prefix[right + 1] - prefix[left]


# ---------------------------------------------------------------------------
# Exemple 2 : Sous-tableaux de somme k
# LeetCode 560 | O(n)
# ---------------------------------------------------------------------------
def subarray_sum(nums: list[int], k: int) -> int:
    count = 0
    prefix = 0
    freq: dict[int, int] = {0: 1}

    for num in nums:
        prefix += num
        count += freq.get(prefix - k, 0)
        freq[prefix] = freq.get(prefix, 0) + 1
    return count


# ---------------------------------------------------------------------------
# Exemple 3 : Equilibre 0/1 (transformer 0 en -1)
# LeetCode 525
# ---------------------------------------------------------------------------
def find_max_length(nums: list[int]) -> int:
    first_index: dict[int, int] = {0: -1}
    prefix = 0
    best = 0

    for i, num in enumerate(nums):
        prefix += 1 if num == 1 else -1
        if prefix in first_index:
            best = max(best, i - first_index[prefix])
        else:
            first_index[prefix] = i
    return best


# ---------------------------------------------------------------------------
# Exemple 4 : Product of array except self (prefix + suffix)
# LeetCode 238 | O(n)
# ---------------------------------------------------------------------------
def product_except_self(nums: list[int]) -> list[int]:
    n = len(nums)
    answer = [1] * n

    prefix = 1
    for i in range(n):
        answer[i] = prefix
        prefix *= nums[i]

    suffix = 1
    for i in range(n - 1, -1, -1):
        answer[i] *= suffix
        suffix *= nums[i]
    return answer


# ---------------------------------------------------------------------------
# Exemple 5 : 2D prefix sum pour requetes sur sous-matrice
# ---------------------------------------------------------------------------
class NumMatrix:
    def __init__(self, matrix: list[list[int]]):
        rows, cols = len(matrix), len(matrix[0]) if matrix else 0
        self.prefix = [[0] * (cols + 1) for _ in range(rows + 1)]
        for r in range(rows):
            for c in range(cols):
                self.prefix[r + 1][c + 1] = (
                    matrix[r][c]
                    + self.prefix[r][c + 1]
                    + self.prefix[r + 1][c]
                    - self.prefix[r][c]
                )

    def sum_region(self, r1: int, c1: int, r2: int, c2: int) -> int:
        p = self.prefix
        return p[r2 + 1][c2 + 1] - p[r1][c2 + 1] - p[r2 + 1][c1] + p[r1][c1]


def run_tests() -> None:
    nums = [1, 2, 3, 4, 5]
    prefix = build_prefix(nums)
    assert prefix == [0, 1, 3, 6, 10, 15]
    assert range_sum(prefix, 1, 3) == 9

    assert subarray_sum([1, 1, 1], 2) == 2
    assert find_max_length([0, 1, 0]) == 2
    assert product_except_self([1, 2, 3, 4]) == [24, 12, 8, 6]

    matrix = NumMatrix([[3, 0, 1, 4, 2], [5, 6, 3, 2, 1], [1, 2, 0, 1, 5], [4, 1, 0, 1, 7], [1, 0, 3, 0, 5]])
    assert matrix.sum_region(2, 1, 4, 3) == 8

    # Bonus : accumulate (stdlib)
    assert list(accumulate(nums)) == [1, 3, 6, 10, 15]
    print("Tous les tests prefix_sum OK")


if __name__ == "__main__":
    run_tests()
