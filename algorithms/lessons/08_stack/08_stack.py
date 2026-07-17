"""
8. Stack (pile LIFO)
====================
Last In, First Out — utile pour parentheses, parsing, DFS iteratif.

En Python : list avec append() et pop()
"""

# ---------------------------------------------------------------------------
# Exemple 1 : Parentheses valides
# LeetCode 20 | O(n)
# ---------------------------------------------------------------------------
def is_valid_parentheses(s: str) -> bool:
    stack: list[str] = []
    pairs = {")": "(", "]": "[", "}": "{"}

    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif not stack or stack.pop() != pairs[ch]:
            return False
    return not stack


# ---------------------------------------------------------------------------
# Exemple 2 : Evaluate Reverse Polish Notation
# LeetCode 150
# ---------------------------------------------------------------------------
def eval_rpn(tokens: list[str]) -> int:
    stack: list[int] = []
    ops = {"+", "-", "*", "/"}

    for token in tokens:
        if token in ops:
            b, a = stack.pop(), stack.pop()
            if token == "+":
                stack.append(a + b)
            elif token == "-":
                stack.append(a - b)
            elif token == "*":
                stack.append(a * b)
            else:
                stack.append(int(a / b))
        else:
            stack.append(int(token))
    return stack[0]


# ---------------------------------------------------------------------------
# Exemple 3 : Min Stack
# LeetCode 155
# ---------------------------------------------------------------------------
class MinStack:
    def __init__(self):
        self.stack: list[int] = []
        self.min_stack: list[int] = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)

    def pop(self) -> None:
        if self.stack.pop() == self.min_stack[-1]:
            self.min_stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def get_min(self) -> int:
        return self.min_stack[-1]


# ---------------------------------------------------------------------------
# Exemple 4 : Daily Temperatures (stack decroissante basique)
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
# Exemple 5 : Simplifier un chemin Unix
# LeetCode 71
# ---------------------------------------------------------------------------
def simplify_path(path: str) -> str:
    stack: list[str] = []
    for part in path.split("/"):
        if part in ("", "."):
            continue
        if part == "..":
            if stack:
                stack.pop()
        else:
            stack.append(part)
    return "/" + "/".join(stack)


def run_tests() -> None:
    assert is_valid_parentheses("()[]{}") is True
    assert is_valid_parentheses("(]") is False
    assert eval_rpn(["2", "1", "+", "3", "*"]) == 9
    assert eval_rpn(["4", "13", "5", "/", "+"]) == 6

    ms = MinStack()
    ms.push(-2)
    ms.push(0)
    ms.push(-3)
    assert ms.get_min() == -3
    ms.pop()
    assert ms.top() == 0
    assert ms.get_min() == -2

    assert daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0]
    assert simplify_path("/home//foo/") == "/home/foo"
    print("Tous les tests stack OK")


if __name__ == "__main__":
    run_tests()
