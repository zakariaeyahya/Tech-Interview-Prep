"""
13. Merge Intervals (fusion d'intervalles)
==========================================
On trie les intervalles par debut, puis on parcourt : si le courant
chevauche le dernier fusionne, on etend ; sinon on ajoute un nouvel
intervalle.

Idee cle : apres tri, deux intervalles se chevauchent ssi
start_courant <= end_precedent.
"""


# ---------------------------------------------------------------------------
# Exemple 1 : Fusionner les intervalles qui se chevauchent
# LeetCode 56 | O(n log n)
# ---------------------------------------------------------------------------
def merge(intervals: list[list[int]]) -> list[list[int]]:
    intervals.sort(key=lambda p: p[0])
    result: list[list[int]] = []
    for start, end in intervals:
        if result and start <= result[-1][1]:
            result[-1][1] = max(result[-1][1], end)
        else:
            result.append([start, end])
    return result


# ---------------------------------------------------------------------------
# Exemple 2 : Inserer un intervalle dans une liste triee sans chevauchement
# LeetCode 57 | O(n)
# ---------------------------------------------------------------------------
def insert(intervals: list[list[int]], new: list[int]) -> list[list[int]]:
    result: list[list[int]] = []
    i, n = 0, len(intervals)

    # Avant le nouvel intervalle
    while i < n and intervals[i][1] < new[0]:
        result.append(intervals[i])
        i += 1

    # Fusion des chevauchements
    while i < n and intervals[i][0] <= new[1]:
        new[0] = min(new[0], intervals[i][0])
        new[1] = max(new[1], intervals[i][1])
        i += 1
    result.append(new)

    # Apres
    while i < n:
        result.append(intervals[i])
        i += 1
    return result


# ---------------------------------------------------------------------------
# Exemple 3 : Intersection de deux listes d'intervalles
# LeetCode 986 | O(n + m)
# ---------------------------------------------------------------------------
def interval_intersection(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    result: list[list[int]] = []
    i = j = 0
    while i < len(a) and j < len(b):
        lo = max(a[i][0], b[j][0])
        hi = min(a[i][1], b[j][1])
        if lo <= hi:
            result.append([lo, hi])
        # Avancer celui qui finit le plus tot
        if a[i][1] < b[j][1]:
            i += 1
        else:
            j += 1
    return result


# ---------------------------------------------------------------------------
# Exemple 4 : Nombre minimal de salles de reunion (balayage debut/fin)
# LeetCode 253 | O(n log n)
# ---------------------------------------------------------------------------
def min_meeting_rooms(intervals: list[list[int]]) -> int:
    starts = sorted(i[0] for i in intervals)
    ends = sorted(i[1] for i in intervals)
    rooms = max_rooms = 0
    s = e = 0
    while s < len(starts):
        if starts[s] < ends[e]:
            rooms += 1                       # une reunion commence
            max_rooms = max(max_rooms, rooms)
            s += 1
        else:
            rooms -= 1                       # une reunion se termine
            e += 1
    return max_rooms


def run_tests() -> None:
    assert merge([[1, 3], [2, 6], [8, 10], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]
    assert merge([[1, 4], [4, 5]]) == [[1, 5]]

    assert insert([[1, 3], [6, 9]], [2, 5]) == [[1, 5], [6, 9]]
    assert insert([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]) == [
        [1, 2], [3, 10], [12, 16]
    ]

    assert interval_intersection(
        [[0, 2], [5, 10], [13, 23], [24, 25]],
        [[1, 5], [8, 12], [15, 24], [25, 26]],
    ) == [[1, 2], [5, 5], [8, 10], [15, 23], [24, 24], [25, 25]]

    assert min_meeting_rooms([[0, 30], [5, 10], [15, 20]]) == 2
    assert min_meeting_rooms([[7, 10], [2, 4]]) == 1

    print("Tous les tests merge_intervals OK")


if __name__ == "__main__":
    run_tests()
