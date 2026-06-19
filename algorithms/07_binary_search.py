"""
7. Binary Search (recherche dichotomique)
=========================================
Recherche O(log n) sur un espace trie ou monotone.

Pattern :
- left, right = bornes
- while left <= right (ou left < right selon variante)
- mid = left + (right - left) // 2
"""

# ---------------------------------------------------------------------------
# Exemple 1 : Recherche classique
# ---------------------------------------------------------------------------
def binary_search(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1


# ---------------------------------------------------------------------------
# Exemple 2 : First / last position (bis repetita)
# LeetCode 34
# ---------------------------------------------------------------------------
def search_range(nums: list[int], target: int) -> list[int]:
    def find_bound(is_first: bool) -> int:
        left, right = 0, len(nums) - 1
        result = -1
        while left <= right:
            mid = left + (right - left) // 2
            if nums[mid] == target:
                result = mid
                if is_first:
                    right = mid - 1
                else:
                    left = mid + 1
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return result

    return [find_bound(True), find_bound(False)]


# ---------------------------------------------------------------------------
# Exemple 3 : Search in rotated sorted array
# LeetCode 33
# ---------------------------------------------------------------------------
def search_rotated(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid

        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    return -1


# ---------------------------------------------------------------------------
# Exemple 4 : Recherche binaire sur reponse (monotone)
# LeetCode 875 — Koko eating bananas
# ---------------------------------------------------------------------------
def min_eating_speed(piles: list[int], h: int) -> int:
    def hours_needed(speed: int) -> int:
        total = 0
        for pile in piles:
            total += (pile + speed - 1) // speed
        return total

    left, right = 1, max(piles)
    while left < right:
        mid = left + (right - left) // 2
        if hours_needed(mid) <= h:
            right = mid
        else:
            left = mid + 1
    return left


# ---------------------------------------------------------------------------
# Exemple 5 : sqrt(x) entier
# LeetCode 69
# ---------------------------------------------------------------------------
def my_sqrt(x: int) -> int:
    if x < 2:
        return x
    left, right = 1, x // 2
    while left <= right:
        mid = left + (right - left) // 2
        square = mid * mid
        if square == x:
            return mid
        if square < x:
            left = mid + 1
        else:
            right = mid - 1
    return right


# ---------------------------------------------------------------------------
# Exemple 6 : Lower bound (premier index >= target)
# ---------------------------------------------------------------------------
def lower_bound(nums: list[int], target: int) -> int:
    left, right = 0, len(nums)
    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid
    return left


def run_tests() -> None:
    nums = [1, 3, 5, 7, 9, 11]
    assert binary_search(nums, 7) == 3
    assert binary_search(nums, 6) == -1
    assert search_range([5, 7, 7, 8, 8, 10], 8) == [3, 4]
    assert search_rotated([4, 5, 6, 7, 0, 1, 2], 0) == 4
    assert min_eating_speed([3, 6, 7, 11], 8) == 4
    assert my_sqrt(8) == 2
    assert lower_bound([1, 2, 2, 4], 2) == 1
    print("Tous les tests binary_search OK")


if __name__ == "__main__":
    run_tests()
