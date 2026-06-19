"""
3. Two Pointers (deux pointeurs)
================================
Deux indices qui avancent selon une regle. Souvent sur un tableau trie.

Variantes :
- Opposes (left/right)
- Meme direction (slow/fast)
"""

# ---------------------------------------------------------------------------
# Exemple 1 : Palindrome (ignorer non-alphanumeriques)
# LeetCode 125 | O(n)
# ---------------------------------------------------------------------------
def is_palindrome(s: str) -> bool:
    left, right = 0, len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True


# ---------------------------------------------------------------------------
# Exemple 2 : Two Sum II sur tableau trie
# LeetCode 167 | O(n)
# ---------------------------------------------------------------------------
def two_sum_sorted(numbers: list[int], target: int) -> list[int]:
    left, right = 0, len(numbers) - 1
    while left < right:
        current = numbers[left] + numbers[right]
        if current == target:
            return [left + 1, right + 1]
        if current < target:
            left += 1
        else:
            right -= 1
    return []


# ---------------------------------------------------------------------------
# Exemple 3 : Retirer les doublons in-place (tableau trie)
# LeetCode 26 | O(n)
# ---------------------------------------------------------------------------
def remove_duplicates(nums: list[int]) -> int:
    if not nums:
        return 0
    write = 1
    for read in range(1, len(nums)):
        if nums[read] != nums[write - 1]:
            nums[write] = nums[read]
            write += 1
    return write


# ---------------------------------------------------------------------------
# Exemple 4 : Container with most water
# LeetCode 11 | O(n)
# ---------------------------------------------------------------------------
def max_area(height: list[int]) -> int:
    left, right = 0, len(height) - 1
    best = 0
    while left < right:
        width = right - left
        best = max(best, width * min(height[left], height[right]))
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    return best


# ---------------------------------------------------------------------------
# Exemple 5 : Cycle dans une linked list (Floyd)
# slow / fast pointers
# ---------------------------------------------------------------------------
class ListNode:
    def __init__(self, val: int = 0, next: "ListNode | None" = None):
        self.val = val
        self.next = next


def has_cycle(head: ListNode | None) -> bool:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False


def run_tests() -> None:
    assert is_palindrome("A man, a plan, a canal: Panama") is True
    assert two_sum_sorted([2, 7, 11, 15], 9) == [1, 2]
    nums = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
    assert remove_duplicates(nums) == 5
    assert nums[:5] == [0, 1, 2, 3, 4]
    assert max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49

    node3 = ListNode(3)
    node2 = ListNode(2, node3)
    node1 = ListNode(1, node2)
    node3.next = node1
    assert has_cycle(node1) is True
    assert has_cycle(ListNode(1)) is False
    print("Tous les tests two_pointers OK")


if __name__ == "__main__":
    run_tests()
