"""AdventOfCode 2020 Day10."""
from typing import Dict, List


test_input_1 = """\
28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3\
"""


def get_input() -> str:
    """Get input str."""
    with open("input/day10.txt") as f:
        return f.read()


def get_adapters(input_str: str) -> List[int]:
    """Return sorted adapter."""
    adapters = [0] + [int(i) for i in input_str.strip().split("\n")]
    adapters.sort()
    adapters.append(adapters[-1] + 3)
    return adapters


def get_differences(adapters: List[int]) -> List[int]:
    """Return adapters differences."""
    return [i2 - i1 for i1, i2 in zip(adapters[: len(adapters)], adapters[1:])]  # noqa


def part1(input_str: str):
    """Part1."""
    differences = get_differences(get_adapters(input_str))
    group_differences: Dict[int, int] = {}

    for difference in differences:
        if difference not in group_differences:
            group_differences[difference] = 1
        else:
            group_differences[difference] += 1

    return group_differences.get(1, 0) * group_differences.get(3, 0)


def part2(input_str: str):
    """Part2."""
    adapters = get_adapters(input_str)

    sol: Dict[int, int] = {0: 1}

    for adapter in adapters[1:]:
        sol[adapter] = 0
        if adapter - 1 in sol:
            sol[adapter] += sol.get(adapter - 1, 1)

        if adapter - 2 in sol:
            sol[adapter] += sol[adapter - 2]

        if adapter - 3 in sol:
            sol[adapter] += sol[adapter - 3]

    return sol[max(adapters)]


if __name__ == "__main__":
    assert part1(test_input_1) == 220
    print(f"Part1: {part1(get_input())}")
    assert part2(test_input_1) == 19208
    print(f"Part2: {part2(get_input())}")
