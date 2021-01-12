"""AdventOfCode 2020 day9."""
from typing import Deque
from typing import List
from collections import deque


def get_input() -> str:
    """Get input str."""
    with open("input/day9.txt") as f:
        return f.read()


def part1(input_str: str, preamble: int) -> int:
    """Part1."""
    return valid([int(s) for s in input_str.strip().split("\n")], preamble)


def part2(input_str: str, preamble: int) -> int:
    """Part2."""
    numbers = [int(s) for s in input_str.strip().split("\n")]
    invalid_num = valid(numbers, preamble)

    window: Deque[int] = deque()
    window_sum = 0

    for n in numbers:
        window.append(n)
        window_sum += n
        while window_sum > invalid_num:
            window_sum -= window.popleft()
        if window_sum == invalid_num:
            return max(window) + min(window)
    return False


def valid(numbers: List[int], preamble: int) -> int:
    """Find valid number."""
    for idx, n in enumerate(numbers[preamble:]):

        candidates = numbers[idx : preamble + idx]  # noqa
        find_candidate = False
        for candidate in candidates.copy():
            if not (n - candidate) in candidates:
                candidates.remove(candidate)
            else:
                find_candidate = True
                break
        if not find_candidate:
            return n
    return True


test_input_1 = """\
35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576\
"""


if __name__ == "__main__":
    assert part1(test_input_1, 5) == 127
    print(part1(get_input(), 25))
    assert part2(test_input_1, 5) == 62
    print(part2(get_input(), 25))
