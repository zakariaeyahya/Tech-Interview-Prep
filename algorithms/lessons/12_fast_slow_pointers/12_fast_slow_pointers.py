"""
12. Fast & Slow Pointers (lievre et tortue / Floyd)
===================================================
Deux pointeurs avancent a des vitesses differentes (slow +1, fast +2).
Le pointeur rapide "rattrape" le lent : detecte les cycles, trouve le
milieu, et repere les repetitions sans memoire supplementaire.

Idee cle : dans un cycle, fast finit toujours par rejoindre slow.
"""

from typing import Optional


class ListNode:
    def __init__(self, val: int = 0, nxt: "Optional[ListNode]" = None):
        self.val = val
        self.next = nxt


# ---------------------------------------------------------------------------
# Exemple 1 : Detecter un cycle dans une liste chainee
# LeetCode 141 | O(n) temps, O(1) espace
# ---------------------------------------------------------------------------
def has_cycle(head: Optional[ListNode]) -> bool:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False


# ---------------------------------------------------------------------------
# Exemple 2 : Trouver le debut du cycle
# LeetCode 142 | O(n)
# ---------------------------------------------------------------------------
def detect_cycle_start(head: Optional[ListNode]) -> Optional[ListNode]:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            # Deuxieme phase : repartir de la tete
            ptr = head
            while ptr is not slow:
                ptr = ptr.next
                slow = slow.next
            return ptr
    return None


# ---------------------------------------------------------------------------
# Exemple 3 : Milieu de la liste chainee
# LeetCode 876 | O(n)
# ---------------------------------------------------------------------------
def middle_node(head: Optional[ListNode]) -> Optional[ListNode]:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow


# ---------------------------------------------------------------------------
# Exemple 4 : Happy Number (cycle sur les sommes de carres)
# LeetCode 202 | O(log n)
# ---------------------------------------------------------------------------
def is_happy(n: int) -> bool:
    def squares(x: int) -> int:
        total = 0
        while x:
            x, digit = divmod(x, 10)
            total += digit * digit
        return total

    slow, fast = n, squares(n)
    while fast != 1 and slow != fast:
        slow = squares(slow)
        fast = squares(squares(fast))
    return fast == 1


# ---------------------------------------------------------------------------
# Exemple 5 : Trouver le nombre duplique (tableau vu comme liste chainee)
# LeetCode 287 | O(n) temps, O(1) espace
# ---------------------------------------------------------------------------
def find_duplicate(nums: list[int]) -> int:
    slow = fast = nums[0]
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
    return slow


# --- Utilitaire de test -----------------------------------------------------
def build_list(values: list[int], cycle_pos: int = -1) -> Optional[ListNode]:
    nodes = [ListNode(v) for v in values]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    if cycle_pos >= 0 and nodes:
        nodes[-1].next = nodes[cycle_pos]
    return nodes[0] if nodes else None


def run_tests() -> None:
    # Cycle
    assert has_cycle(build_list([3, 2, 0, -4], cycle_pos=1)) is True
    assert has_cycle(build_list([1, 2])) is False

    # Debut de cycle
    start = detect_cycle_start(build_list([3, 2, 0, -4], cycle_pos=1))
    assert start is not None and start.val == 2

    # Milieu
    assert middle_node(build_list([1, 2, 3, 4, 5])).val == 3
    assert middle_node(build_list([1, 2, 3, 4])).val == 3  # second milieu

    # Happy number
    assert is_happy(19) is True
    assert is_happy(2) is False

    # Nombre duplique
    assert find_duplicate([1, 3, 4, 2, 2]) == 2
    assert find_duplicate([3, 1, 3, 4, 2]) == 3

    print("Tous les tests fast_slow_pointers OK")


if __name__ == "__main__":
    run_tests()
