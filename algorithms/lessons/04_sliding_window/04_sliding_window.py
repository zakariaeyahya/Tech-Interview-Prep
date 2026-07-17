"""
4. Sliding Window (fenetre glissante)
=====================================
Maintenir une fenetre [left, right] et l'ajuster selon une contrainte.

Cas d'usage :
- Sous-chaine / sous-tableau de longueur fixe ou variable
- Maximum/minimum sur une fenetre
"""

from collections import Counter, defaultdict


# ---------------------------------------------------------------------------
# Exemple 1 : Longueur max sous-tableau de somme <= k
# O(n)
# ---------------------------------------------------------------------------
def max_subarray_len_sum_at_most(nums: list[int], k: int) -> int:
    left = 0
    window_sum = 0
    best = 0

    for right, num in enumerate(nums):
        window_sum += num
        while window_sum > k and left <= right:
            window_sum -= nums[left]
            left += 1
        best = max(best, right - left + 1)
    return best


# ---------------------------------------------------------------------------
# Exemple 2 : Longueur min sous-tableau avec somme >= target
# LeetCode 209 | O(n)
# ---------------------------------------------------------------------------
def min_subarray_len(target: int, nums: list[int]) -> int:
    left = 0
    window_sum = 0
    best = float("inf")

    for right, num in enumerate(nums):
        window_sum += num
        while window_sum >= target:
            best = min(best, right - left + 1)
            window_sum -= nums[left]
            left += 1
    return 0 if best == float("inf") else best


# ---------------------------------------------------------------------------
# Exemple 3 : Longueur max sous-chaine sans repetition
# LeetCode 3 | O(n)
# ---------------------------------------------------------------------------
def length_of_longest_substring(s: str) -> int:
    last_seen: dict[str, int] = {}
    left = 0
    best = 0

    for right, ch in enumerate(s):
        if ch in last_seen and last_seen[ch] >= left:
            left = last_seen[ch] + 1
        last_seen[ch] = right
        best = max(best, right - left + 1)
    return best


# ---------------------------------------------------------------------------
# Exemple 4 : Anagrammes dans une chaine
# LeetCode 438 | O(n)
# ---------------------------------------------------------------------------
def find_anagrams(s: str, p: str) -> list[int]:
    if len(p) > len(s):
        return []

    need = Counter(p)
    window: dict[str, int] = defaultdict(int)
    result: list[int] = []
    left = 0
    matched = 0
    required = len(need)

    for right, ch in enumerate(s):
        window[ch] += 1
        if ch in need and window[ch] == need[ch]:
            matched += 1

        while right - left + 1 >= len(p):
            if matched == required:
                result.append(left)
            left_char = s[left]
            if left_char in need and window[left_char] == need[left_char]:
                matched -= 1
            window[left_char] -= 1
            left += 1
    return result


# ---------------------------------------------------------------------------
# Exemple 5 : Fenetre fixe — max somme de k elements consecutifs
# O(n)
# ---------------------------------------------------------------------------
def max_sum_subarray_k(nums: list[int], k: int) -> int:
    if len(nums) < k:
        return 0
    window_sum = sum(nums[:k])
    best = window_sum
    for right in range(k, len(nums)):
        window_sum += nums[right] - nums[right - k]
        best = max(best, window_sum)
    return best


def run_tests() -> None:
    assert max_subarray_len_sum_at_most([1, 2, 1, 0, 1, 1, 0], 4) == 5
    assert min_subarray_len(7, [2, 3, 1, 2, 4, 3]) == 2
    assert length_of_longest_substring("abcabcbb") == 3
    assert find_anagrams("cbaebabacd", "abc") == [0, 6]
    assert max_sum_subarray_k([2, 1, 5, 1, 3, 2], 3) == 9
    print("Tous les tests sliding_window OK")


if __name__ == "__main__":
    run_tests()
