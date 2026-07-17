"""
1. Hash Map / Dictionary
========================
Structure cle -> valeur pour acces O(1) en moyenne.

Cas d'usage typiques :
- Compter des frequences
- Stocker des indices / complements deja vus
- Grouper des elements par cle
"""

from collections import Counter, defaultdict


# ---------------------------------------------------------------------------
# Exemple 1 : Two Sum — trouver 2 indices dont la somme = target
# LeetCode 1 | O(n) temps, O(n) espace
# ---------------------------------------------------------------------------
def two_sum(nums: list[int], target: int) -> list[int]:
    seen: dict[int, int] = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []


# ---------------------------------------------------------------------------
# Exemple 2 : Grouper les anagrammes
# LeetCode 49 | O(n * k log k) si tri de la cle, O(n * k) avec comptage
# ---------------------------------------------------------------------------
def group_anagrams(words: list[str]) -> list[list[str]]:
    groups: dict[tuple, list[str]] = defaultdict(list)
    for word in words:
        key = tuple(sorted(word))
        groups[key].append(word)
    return list(groups.values())


# ---------------------------------------------------------------------------
# Exemple 3 : Sous-tableau de somme nulle (longueur max)
# O(n) — prefix_sum indexe dans un dict
# ---------------------------------------------------------------------------
def max_subarray_sum_zero(nums: list[int]) -> int:
    first_index: dict[int, int] = {0: -1}
    prefix = 0
    best = 0

    for i, num in enumerate(nums):
        prefix += num
        if prefix in first_index:
            best = max(best, i - first_index[prefix])
        else:
            first_index[prefix] = i
    return best


# ---------------------------------------------------------------------------
# Exemple 4 : Compter les frequences
# ---------------------------------------------------------------------------
def top_k_frequent(nums: list[int], k: int) -> list[int]:
    counts = Counter(nums)
    return [num for num, _ in counts.most_common(k)]


# ---------------------------------------------------------------------------
# Exemple 5 : Verifier si 2 chaines sont isomorphiques
# LeetCode 205
# ---------------------------------------------------------------------------
def is_isomorphic(s: str, t: str) -> bool:
    s_to_t: dict[str, str] = {}
    t_to_s: dict[str, str] = {}

    for a, b in zip(s, t):
        if s_to_t.get(a, b) != b or t_to_s.get(b, a) != a:
            return False
        s_to_t[a] = b
        t_to_s[b] = a
    return True


def run_tests() -> None:
    assert two_sum([2, 7, 11, 15], 9) == [0, 1]
    assert sorted(group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])) == sorted(
        [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
    )
    assert max_subarray_sum_zero([15, -2, 2, -8, 1, 7, 10, 23]) == 5
    assert top_k_frequent([1, 1, 1, 2, 2, 3], 2) == [1, 2]
    assert is_isomorphic("egg", "add") is True
    assert is_isomorphic("foo", "bar") is False
    print("Tous les tests hash_map OK")


if __name__ == "__main__":
    run_tests()
