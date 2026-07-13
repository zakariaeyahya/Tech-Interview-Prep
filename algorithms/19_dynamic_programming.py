"""
19. Dynamic Programming (programmation dynamique)
=================================================
On decompose un probleme en sous-problemes qui se chevauchent, et on
memorise leurs solutions pour ne les calculer qu'une fois.

Deux styles :
  - top-down : recursion + memoisation (dictionnaire / lru_cache).
  - bottom-up : tableau dp rempli iterativement.

Reconnaitre : "nombre de facons", "min/max cout", "possible ou non",
sous-structure optimale + sous-problemes qui se repetent.
"""

from functools import lru_cache


# ---------------------------------------------------------------------------
# Exemple 1 : Grimper des escaliers (Fibonacci deguise)
# LeetCode 70 | O(n) temps, O(1) espace
# ---------------------------------------------------------------------------
def climb_stairs(n: int) -> int:
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a


# ---------------------------------------------------------------------------
# Exemple 2 : Coin Change (min de pieces) - bottom-up
# LeetCode 322 | O(montant * pieces)
# ---------------------------------------------------------------------------
def coin_change(coins: list[int], amount: int) -> int:
    dp = [float("inf")] * (amount + 1)
    dp[0] = 0
    for coin in coins:
        for x in range(coin, amount + 1):
            dp[x] = min(dp[x], dp[x - coin] + 1)
    return dp[amount] if dp[amount] != float("inf") else -1


# ---------------------------------------------------------------------------
# Exemple 3 : House Robber (choisir sans voisins adjacents)
# LeetCode 198 | O(n) temps, O(1) espace
# ---------------------------------------------------------------------------
def rob(nums: list[int]) -> int:
    prev = curr = 0
    for x in nums:
        prev, curr = curr, max(curr, prev + x)
    return curr


# ---------------------------------------------------------------------------
# Exemple 4 : Longest Increasing Subsequence (LIS)
# LeetCode 300 | O(n^2)
# ---------------------------------------------------------------------------
def length_of_lis(nums: list[int]) -> int:
    if not nums:
        return 0
    dp = [1] * len(nums)
    for i in range(len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)


# ---------------------------------------------------------------------------
# Exemple 5 : 0/1 Knapsack (sac a dos) - top-down memoise
# O(n * capacite)
# ---------------------------------------------------------------------------
def knapsack(weights: list[int], values: list[int], capacity: int) -> int:
    @lru_cache(maxsize=None)
    def best(i: int, cap: int) -> int:
        if i == len(weights) or cap == 0:
            return 0
        skip = best(i + 1, cap)                 # ne pas prendre l'objet i
        take = 0
        if weights[i] <= cap:                   # prendre l'objet i
            take = values[i] + best(i + 1, cap - weights[i])
        return max(skip, take)

    return best(0, capacity)


def run_tests() -> None:
    assert climb_stairs(2) == 2
    assert climb_stairs(5) == 8

    assert coin_change([1, 2, 5], 11) == 3      # 5 + 5 + 1
    assert coin_change([2], 3) == -1

    assert rob([1, 2, 3, 1]) == 4               # 1 + 3
    assert rob([2, 7, 9, 3, 1]) == 12           # 2 + 9 + 1

    assert length_of_lis([10, 9, 2, 5, 3, 7, 101, 18]) == 4
    assert length_of_lis([0, 1, 0, 3, 2, 3]) == 4

    assert knapsack([1, 3, 4, 5], [1, 4, 5, 7], 7) == 9  # objets 3+4 -> poids 7, valeur 9
    assert knapsack([2, 3, 4], [3, 4, 5], 5) == 7        # objets 2+3 -> valeur 7

    print("Tous les tests dynamic_programming OK")


if __name__ == "__main__":
    run_tests()
