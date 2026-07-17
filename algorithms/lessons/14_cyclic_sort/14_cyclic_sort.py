"""
14. Cyclic Sort (tri cyclique)
==============================
Quand un tableau contient des nombres dans une plage connue [1..n]
(ou [0..n]), on place chaque valeur a son index correct en echangeant.
Apres ce placement, tout index dont la valeur ne correspond pas revele
un manquant ou un duplique.

Idee cle : la valeur v doit aller a l'index v-1 (plage 1..n).
Cout O(n) sans memoire supplementaire.
"""


# ---------------------------------------------------------------------------
# Exemple 1 : Tri cyclique de base (valeurs 1..n)
# O(n)
# ---------------------------------------------------------------------------
def cyclic_sort(nums: list[int]) -> list[int]:
    i = 0
    while i < len(nums):
        correct = nums[i] - 1                 # place attendue de nums[i]
        if nums[i] != nums[correct]:
            nums[i], nums[correct] = nums[correct], nums[i]
        else:
            i += 1
    return nums


# ---------------------------------------------------------------------------
# Exemple 2 : Nombre manquant (plage 0..n)
# LeetCode 268 | O(n)
# ---------------------------------------------------------------------------
def missing_number(nums: list[int]) -> int:
    i, n = 0, len(nums)
    while i < n:
        j = nums[i]
        if j < n and nums[i] != nums[j]:
            nums[i], nums[j] = nums[j], nums[i]
        else:
            i += 1
    for idx in range(n):
        if nums[idx] != idx:
            return idx
    return n


# ---------------------------------------------------------------------------
# Exemple 3 : Tous les nombres disparus (plage 1..n)
# LeetCode 448 | O(n)
# ---------------------------------------------------------------------------
def find_disappeared_numbers(nums: list[int]) -> list[int]:
    i = 0
    while i < len(nums):
        correct = nums[i] - 1
        if nums[i] != nums[correct]:
            nums[i], nums[correct] = nums[correct], nums[i]
        else:
            i += 1
    return [idx + 1 for idx, v in enumerate(nums) if v != idx + 1]


# ---------------------------------------------------------------------------
# Exemple 4 : Trouver le duplique et le manquant
# LeetCode 645 | O(n)
# ---------------------------------------------------------------------------
def find_error_nums(nums: list[int]) -> list[int]:
    i = 0
    while i < len(nums):
        correct = nums[i] - 1
        if nums[i] != nums[correct]:
            nums[i], nums[correct] = nums[correct], nums[i]
        else:
            i += 1
    for idx in range(len(nums)):
        if nums[idx] != idx + 1:
            return [nums[idx], idx + 1]       # [duplique, manquant]
    return []


def run_tests() -> None:
    assert cyclic_sort([3, 1, 5, 4, 2]) == [1, 2, 3, 4, 5]
    assert cyclic_sort([2, 6, 4, 3, 1, 5]) == [1, 2, 3, 4, 5, 6]

    assert missing_number([3, 0, 1]) == 2
    assert missing_number([0, 1]) == 2
    assert missing_number([9, 6, 4, 2, 3, 5, 7, 0, 1]) == 8

    assert find_disappeared_numbers([4, 3, 2, 7, 8, 2, 3, 1]) == [5, 6]
    assert find_disappeared_numbers([1, 1]) == [2]

    assert find_error_nums([1, 2, 2, 4]) == [2, 3]
    assert find_error_nums([3, 2, 2]) == [2, 1]

    print("Tous les tests cyclic_sort OK")


if __name__ == "__main__":
    run_tests()
