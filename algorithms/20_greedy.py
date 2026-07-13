"""
20. Greedy (algorithme glouton)
===============================
A chaque etape, on fait le choix localement optimal en esperant qu'il
mene a l'optimum global. Rapide (souvent O(n log n) avec un tri), mais
ne marche que si le probleme a la propriete du "choix glouton".

Difference avec la DP : le glouton ne revient jamais en arriere ; il faut
prouver (ou reconnaitre) que le choix local est sur.
"""


# ---------------------------------------------------------------------------
# Exemple 1 : Jump Game - peut-on atteindre la fin ?
# LeetCode 55 | O(n)
# ---------------------------------------------------------------------------
def can_jump(nums: list[int]) -> bool:
    reachable = 0
    for i, jump in enumerate(nums):
        if i > reachable:                       # trou infranchissable
            return False
        reachable = max(reachable, i + jump)
    return True


# ---------------------------------------------------------------------------
# Exemple 2 : Nombre minimal de sauts
# LeetCode 45 | O(n)
# ---------------------------------------------------------------------------
def jump(nums: list[int]) -> int:
    jumps = current_end = farthest = 0
    for i in range(len(nums) - 1):
        farthest = max(farthest, i + nums[i])
        if i == current_end:                    # fin de la portee actuelle
            jumps += 1
            current_end = farthest
    return jumps


# ---------------------------------------------------------------------------
# Exemple 3 : Intervalles non chevauchants a retirer
# LeetCode 435 | O(n log n)
# ---------------------------------------------------------------------------
def erase_overlap_intervals(intervals: list[list[int]]) -> int:
    intervals.sort(key=lambda p: p[1])          # trier par fin
    removed, prev_end = 0, float("-inf")
    for start, end in intervals:
        if start >= prev_end:
            prev_end = end                      # garder cet intervalle
        else:
            removed += 1                        # chevauchement -> retirer
    return removed


# ---------------------------------------------------------------------------
# Exemple 4 : Distribuer des bonbons (enfants avec notes)
# LeetCode 135 | O(n)
# ---------------------------------------------------------------------------
def candy(ratings: list[int]) -> int:
    n = len(ratings)
    candies = [1] * n
    for i in range(1, n):                       # passe gauche -> droite
        if ratings[i] > ratings[i - 1]:
            candies[i] = candies[i - 1] + 1
    for i in range(n - 2, -1, -1):              # passe droite -> gauche
        if ratings[i] > ratings[i + 1]:
            candies[i] = max(candies[i], candies[i + 1] + 1)
    return sum(candies)


# ---------------------------------------------------------------------------
# Exemple 5 : Meilleur moment pour acheter/vendre (transactions multiples)
# LeetCode 122 | O(n)
# ---------------------------------------------------------------------------
def max_profit(prices: list[int]) -> int:
    profit = 0
    for i in range(1, len(prices)):
        if prices[i] > prices[i - 1]:           # capter chaque hausse
            profit += prices[i] - prices[i - 1]
    return profit


def run_tests() -> None:
    assert can_jump([2, 3, 1, 1, 4]) is True
    assert can_jump([3, 2, 1, 0, 4]) is False

    assert jump([2, 3, 1, 1, 4]) == 2
    assert jump([2, 3, 0, 1, 4]) == 2

    assert erase_overlap_intervals([[1, 2], [2, 3], [3, 4], [1, 3]]) == 1
    assert erase_overlap_intervals([[1, 2], [1, 2], [1, 2]]) == 2

    assert candy([1, 0, 2]) == 5                # 2 + 1 + 2
    assert candy([1, 2, 2]) == 4                # 1 + 2 + 1

    assert max_profit([7, 1, 5, 3, 6, 4]) == 7  # (5-1) + (6-3)
    assert max_profit([1, 2, 3, 4, 5]) == 4

    print("Tous les tests greedy OK")


if __name__ == "__main__":
    run_tests()
