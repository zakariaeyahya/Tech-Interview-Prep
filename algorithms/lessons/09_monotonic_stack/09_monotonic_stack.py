"""
9. Monotonic Stack (pile monotone)
==================================
Pile ou les elements sont toujours croissants ou decroissants.

Cas d'usage :
- Prochain element plus grand/petit
- Largest rectangle in histogram
- Trapping rain water
"""

# ---------------------------------------------------------------------------
# Exemple 1 : Next Greater Element
# LeetCode 496
# ---------------------------------------------------------------------------
def next_greater_element(nums1: list[int], nums2: list[int]) -> list[int]:
    next_greater: dict[int, int] = {}
    stack: list[int] = []

    for num in nums2:
        while stack and stack[-1] < num:
            next_greater[stack.pop()] = num
        stack.append(num)

    return [next_greater.get(num, -1) for num in nums1]


# ---------------------------------------------------------------------------
# Exemple 2 : Daily Temperatures (pile decroissante)
# LeetCode 739
# ---------------------------------------------------------------------------
def daily_temperatures(temperatures: list[int]) -> list[int]:
    result = [0] * len(temperatures)
    stack: list[int] = []

    for i, temp in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < temp:
            prev = stack.pop()
            result[prev] = i - prev
        stack.append(i)
    return result


# ---------------------------------------------------------------------------
# Exemple 3 : Largest Rectangle in Histogram
# LeetCode 84 | O(n)
# ---------------------------------------------------------------------------
def largest_rectangle_area(heights: list[int]) -> int:
    stack: list[int] = []
    best = 0
    heights = heights + [0]

    for i, h in enumerate(heights):
        while stack and h < heights[stack[-1]]:
            height = heights[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            best = max(best, height * width)
        stack.append(i)
    return best


# ---------------------------------------------------------------------------
# Exemple 4 : Trapping Rain Water
# LeetCode 42 | O(n) avec monotonic stack
# ---------------------------------------------------------------------------
def trap(height: list[int]) -> int:
    stack: list[int] = []
    water = 0

    for i, h in enumerate(height):
        while stack and h > height[stack[-1]]:
            bottom = stack.pop()
            if not stack:
                break
            width = i - stack[-1] - 1
            bounded_height = min(h, height[stack[-1]]) - height[bottom]
            water += width * bounded_height
        stack.append(i)
    return water


# ---------------------------------------------------------------------------
# Exemple 5 : Sum of subarray minimums
# LeetCode 907
# ---------------------------------------------------------------------------
def sum_subarray_mins(arr: list[int]) -> int:
    MOD = 10**9 + 7
    n = len(arr)
    prev_less = [-1] * n
    next_less = [n] * n
    stack: list[int] = []

    for i in range(n):
        while stack and arr[stack[-1]] > arr[i]:
            next_less[stack.pop()] = i
        prev_less[i] = stack[-1] if stack else -1
        stack.append(i)

    total = 0
    for i, val in enumerate(arr):
        left = i - prev_less[i]
        right = next_less[i] - i
        total = (total + val * left * right) % MOD
    return total


def run_tests() -> None:
    assert next_greater_element([4, 1, 2], [1, 3, 4, 2]) == [-1, 3, -1]
    assert daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0]
    assert largest_rectangle_area([2, 1, 5, 6, 2, 3]) == 10
    assert trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6
    assert sum_subarray_mins([3, 1, 2, 4]) == 17
    print("Tous les tests monotonic_stack OK")


if __name__ == "__main__":
    run_tests()
