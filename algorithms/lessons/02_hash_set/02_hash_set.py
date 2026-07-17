"""
2. Hash Set
===========
Ensemble de valeurs uniques avec test d'appartenance O(1) en moyenne.

Cas d'usage typiques :
- Detecter les doublons
- Trouver l'intersection / union
- Parcours avec memoire des elements deja vus
"""

# ---------------------------------------------------------------------------
# Exemple 1 : Contient un doublon ?
# LeetCode 217 | O(n) temps, O(n) espace
# ---------------------------------------------------------------------------
def contains_duplicate(nums: list[int]) -> bool:
    seen: set[int] = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False


# ---------------------------------------------------------------------------
# Exemple 2 : Trouver le premier caractere non repete
# ---------------------------------------------------------------------------
def first_unique_char(s: str) -> int:
    seen: set[str] = set()
    repeated: set[str] = set()

    for i, ch in enumerate(s):
        if ch in seen:
            repeated.add(ch)
        else:
            seen.add(ch)

    for i, ch in enumerate(s):
        if ch not in repeated:
            return i
    return -1


# ---------------------------------------------------------------------------
# Exemple 3 : Intersection de 2 tableaux
# LeetCode 349
# ---------------------------------------------------------------------------
def intersection(nums1: list[int], nums2: list[int]) -> list[int]:
    set1 = set(nums1)
    return list({num for num in nums2 if num in set1})


# ---------------------------------------------------------------------------
# Exemple 4 : Longueur de la plus longue sequence consecutive
# LeetCode 128 | O(n)
# ---------------------------------------------------------------------------
def longest_consecutive(nums: list[int]) -> int:
    num_set = set(nums)
    best = 0

    for num in num_set:
        if num - 1 in num_set:
            continue
        current = num
        length = 1
        while current + 1 in num_set:
            current += 1
            length += 1
        best = max(best, length)
    return best


# ---------------------------------------------------------------------------
# Exemple 5 : Happy Number (detecter un cycle avec un set)
# LeetCode 202
# ---------------------------------------------------------------------------
def _sum_squares(n: int) -> int:
    total = 0
    while n:
        n, digit = divmod(n, 10)
        total += digit * digit
    return total


def is_happy(n: int) -> bool:
    seen: set[int] = set()
    while n != 1 and n not in seen:
        seen.add(n)
        n = _sum_squares(n)
    return n == 1


def run_tests() -> None:
    assert contains_duplicate([1, 2, 3, 1]) is True
    assert contains_duplicate([1, 2, 3, 4]) is False
    assert first_unique_char("leetcode") == 0
    assert first_unique_char("aabb") == -1
    assert sorted(intersection([1, 2, 2, 1], [2, 2])) == [2]
    assert longest_consecutive([100, 4, 200, 1, 3, 2]) == 4
    assert is_happy(19) is True
    assert is_happy(2) is False
    print("Tous les tests hash_set OK")


if __name__ == "__main__":
    run_tests()
