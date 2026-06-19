"""
11. Linked List (liste chainee)
===============================
Noeuds avec .val et .next — operations fondamentales pour entretiens.

Attention aux edge cases :
- liste vide
- un seul noeud
- modifier head / tail
"""


class ListNode:
    def __init__(self, val: int = 0, next: "ListNode | None" = None):
        self.val = val
        self.next = next


def build_list(values: list[int]) -> ListNode | None:
    dummy = ListNode()
    current = dummy
    for val in values:
        current.next = ListNode(val)
        current = current.next
    return dummy.next


def list_to_array(head: ListNode | None) -> list[int]:
    result = []
    while head:
        result.append(head.val)
        head = head.next
    return result


# ---------------------------------------------------------------------------
# Exemple 1 : Reverse linked list
# LeetCode 206 | O(n)
# ---------------------------------------------------------------------------
def reverse_list(head: ListNode | None) -> ListNode | None:
    prev = None
    current = head
    while current:
        nxt = current.next
        current.next = prev
        prev = current
        current = nxt
    return prev


# ---------------------------------------------------------------------------
# Exemple 2 : Merge two sorted lists
# LeetCode 21
# ---------------------------------------------------------------------------
def merge_two_lists(l1: ListNode | None, l2: ListNode | None) -> ListNode | None:
    dummy = ListNode()
    tail = dummy

    while l1 and l2:
        if l1.val <= l2.val:
            tail.next = l1
            l1 = l1.next
        else:
            tail.next = l2
            l2 = l2.next
        tail = tail.next
    tail.next = l1 or l2
    return dummy.next


# ---------------------------------------------------------------------------
# Exemple 3 : Detect cycle (Floyd)
# LeetCode 141
# ---------------------------------------------------------------------------
def has_cycle(head: ListNode | None) -> bool:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False


# ---------------------------------------------------------------------------
# Exemple 4 : Middle of linked list
# LeetCode 876
# ---------------------------------------------------------------------------
def middle_node(head: ListNode | None) -> ListNode | None:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow


# ---------------------------------------------------------------------------
# Exemple 5 : Remove Nth node from end
# LeetCode 19 — two pointers avec dummy head
# ---------------------------------------------------------------------------
def remove_nth_from_end(head: ListNode | None, n: int) -> ListNode | None:
    dummy = ListNode(0, head)
    left = right = dummy

    for _ in range(n + 1):
        right = right.next

    while right:
        left = left.next
        right = right.next

    left.next = left.next.next
    return dummy.next


# ---------------------------------------------------------------------------
# Exemple 6 : Reorder list (L0->Ln->L1->Ln-1...)
# LeetCode 143
# ---------------------------------------------------------------------------
def reorder_list(head: ListNode | None) -> None:
    if not head or not head.next:
        return

    slow = fast = head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next

    second = reverse_list(slow.next)
    slow.next = None

    first = head
    while second:
        tmp1, tmp2 = first.next, second.next
        first.next = second
        second.next = tmp1
        first, second = tmp1, tmp2


# ---------------------------------------------------------------------------
# Exemple 7 : Palindrome linked list
# LeetCode 234
# ---------------------------------------------------------------------------
def is_palindrome_list(head: ListNode | None) -> bool:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    second_half = reverse_list(slow)
    first_half = head

    while second_half:
        if first_half.val != second_half.val:
            return False
        first_half = first_half.next
        second_half = second_half.next
    return True


def run_tests() -> None:
    assert list_to_array(reverse_list(build_list([1, 2, 3, 4, 5]))) == [5, 4, 3, 2, 1]
    assert list_to_array(merge_two_lists(build_list([1, 2, 4]), build_list([1, 3, 4]))) == [1, 1, 2, 3, 4, 4]

    node3 = ListNode(3)
    node2 = ListNode(2, node3)
    node1 = ListNode(1, node2)
    node3.next = node1
    assert has_cycle(node1) is True

    assert middle_node(build_list([1, 2, 3, 4, 5])).val == 3
    assert list_to_array(remove_nth_from_end(build_list([1, 2, 3, 4, 5]), 2)) == [1, 2, 3, 5]

    head = build_list([1, 2, 3, 4])
    reorder_list(head)
    assert list_to_array(head) == [1, 4, 2, 3]

    assert is_palindrome_list(build_list([1, 2, 2, 1])) is True
    assert is_palindrome_list(build_list([1, 2])) is False
    print("Tous les tests linked_list OK")


if __name__ == "__main__":
    run_tests()
