"""
6. Sorting (tri)
================
Connaitre les tris courants et quand les utiliser.

Complexites :
- QuickSort / MergeSort : O(n log n)
- Counting sort : O(n + k) si valeurs bornees
- Timsort (Python sorted) : O(n log n), stable
"""

from collections import Counter


# ---------------------------------------------------------------------------
# Exemple 1 : Tri custom avec key
# ---------------------------------------------------------------------------
def sort_by_absolute_value(nums: list[int]) -> list[int]:
    return sorted(nums, key=abs)


def sort_intervals(intervals: list[list[int]]) -> list[list[int]]:
    return sorted(intervals, key=lambda x: (x[0], x[1]))


# ---------------------------------------------------------------------------
# Exemple 2 : Merge intervals
# LeetCode 56 | O(n log n)
# ---------------------------------------------------------------------------
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]

    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged


# ---------------------------------------------------------------------------
# Exemple 3 : Kth largest element
# LeetCode 215 | O(n log n) simple, O(n) avec quickselect
# ---------------------------------------------------------------------------
def find_kth_largest(nums: list[int], k: int) -> int:
    return sorted(nums, reverse=True)[k - 1]


def find_kth_largest_quickselect(nums: list[int], k: int) -> int:
    target = len(nums) - k

    def partition(left: int, right: int) -> int:
        pivot = nums[right]
        store = left
        for i in range(left, right):
            if nums[i] <= pivot:
                nums[store], nums[i] = nums[i], nums[store]
                store += 1
        nums[store], nums[right] = nums[right], nums[store]
        return store

    left, right = 0, len(nums) - 1
    while left <= right:
        pivot_index = partition(left, right)
        if pivot_index == target:
            return nums[pivot_index]
        if pivot_index < target:
            left = pivot_index + 1
        else:
            right = pivot_index - 1
    raise ValueError("k invalide")


# ---------------------------------------------------------------------------
# Exemple 4 : Meeting rooms — detecter conflit
# LeetCode 252
# ---------------------------------------------------------------------------
def can_attend_meetings(intervals: list[list[int]]) -> bool:
    intervals.sort(key=lambda x: x[0])
    for i in range(1, len(intervals)):
        if intervals[i][0] < intervals[i - 1][1]:
            return False
    return True


# ---------------------------------------------------------------------------
# Exemple 5 : Tri par frequence puis valeur
# LeetCode 1636
# ---------------------------------------------------------------------------
def frequency_sort(nums: list[int]) -> list[int]:
    counts = Counter(nums)
    return sorted(nums, key=lambda x: (counts[x], x))


# ---------------------------------------------------------------------------
# Exemple 6 : Counting sort (valeurs non negatives petites)
# ---------------------------------------------------------------------------
def counting_sort(nums: list[int], max_value: int) -> list[int]:
    counts = [0] * (max_value + 1)
    for num in nums:
        counts[num] += 1
    result = []
    for value, freq in enumerate(counts):
        result.extend([value] * freq)
    return result


def run_tests() -> None:
    assert sort_by_absolute_value([-3, 1, -2, 4]) == [1, -2, -3, 4]
    assert merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]
    assert find_kth_largest([3, 2, 1, 5, 6, 4], 2) == 5
    assert find_kth_largest_quickselect([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4
    assert can_attend_meetings([[0, 30], [5, 10], [15, 20]]) is False
    assert frequency_sort([2, 3, 1, 3, 2, 2, 2]) == [1, 3, 3, 2, 2, 2, 2]
    assert counting_sort([4, 2, 2, 8, 3, 3], 8) == [2, 2, 3, 3, 4, 8]
    print("Tous les tests sorting OK")


if __name__ == "__main__":
    run_tests()
