"""
21. Bit Manipulation (manipulation de bits)
===========================================
On travaille directement sur la representation binaire des entiers avec
les operateurs bit a bit. Souvent la solution O(1) espace la plus rapide.

Operateurs cles :
  &  ET      |  OU      ^  XOR      ~  NON      <<  >>  decalages
Astuces :
  x & 1            -> bit de poids faible (parite)
  x & (x - 1)      -> efface le bit 1 le plus a droite
  x ^ x = 0        -> XOR annule les doublons
  x & (-x)         -> isole le bit 1 le plus a droite
"""


# ---------------------------------------------------------------------------
# Exemple 1 : Single Number (tous en double sauf un)
# LeetCode 136 | O(n) temps, O(1) espace
# ---------------------------------------------------------------------------
def single_number(nums: list[int]) -> int:
    result = 0
    for x in nums:
        result ^= x                             # les doublons s'annulent
    return result


# ---------------------------------------------------------------------------
# Exemple 2 : Compter les bits a 1 (Hamming weight)
# LeetCode 191 | O(nb de bits a 1)
# ---------------------------------------------------------------------------
def count_ones(n: int) -> int:
    count = 0
    while n:
        n &= n - 1                              # efface le 1 le plus a droite
        count += 1
    return count


# ---------------------------------------------------------------------------
# Exemple 3 : Puissance de deux ?
# LeetCode 231 | O(1)
# ---------------------------------------------------------------------------
def is_power_of_two(n: int) -> bool:
    return n > 0 and (n & (n - 1)) == 0         # un seul bit a 1


# ---------------------------------------------------------------------------
# Exemple 4 : Nombre manquant via XOR (plage 0..n)
# LeetCode 268 | O(n)
# ---------------------------------------------------------------------------
def missing_number(nums: list[int]) -> int:
    result = len(nums)
    for i, x in enumerate(nums):
        result ^= i ^ x                         # indices XOR valeurs
    return result


# ---------------------------------------------------------------------------
# Exemple 5 : Inverser les bits d'un entier 32 bits
# LeetCode 190 | O(1)
# ---------------------------------------------------------------------------
def reverse_bits(n: int) -> int:
    result = 0
    for _ in range(32):
        result = (result << 1) | (n & 1)        # pousser le bit courant
        n >>= 1
    return result


# ---------------------------------------------------------------------------
# Exemple 6 : Nombre de bits a 1 pour 0..n (DP + bits)
# LeetCode 338 | O(n)
# ---------------------------------------------------------------------------
def counting_bits(n: int) -> list[int]:
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i >> 1] + (i & 1)            # bits(i) = bits(i//2) + dernier bit
    return dp


def run_tests() -> None:
    assert single_number([4, 1, 2, 1, 2]) == 4
    assert single_number([2, 2, 1]) == 1

    assert count_ones(0b1011) == 3
    assert count_ones(0) == 0

    assert is_power_of_two(16) is True
    assert is_power_of_two(18) is False
    assert is_power_of_two(1) is True

    assert missing_number([3, 0, 1]) == 2
    assert missing_number([0, 1]) == 2

    assert reverse_bits(0b00000010100101000001111010011100) == 964176192

    assert counting_bits(5) == [0, 1, 1, 2, 1, 2]

    print("Tous les tests bit_manipulation OK")


if __name__ == "__main__":
    run_tests()
