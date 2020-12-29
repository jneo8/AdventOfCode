"""AdventOfCode 2020 Day6."""
from typing import Dict


def get_input() -> str:
    """Get input as str."""
    with open("input/day6.txt") as f:
        return f.read()


def get_group_count(s: str) -> int:
    """Get group answer count."""
    g = set(s)
    if "\n" in g:
        g.remove("\n")
    return len(g)


def part1(input_str: str):
    """Part1."""
    return sum(get_group_count(group) for group in input_str.split("\n\n"))


def part2(input_str: str):
    """Part2."""
    sum_ = 0
    for group in input_str.split("\n\n"):
        counter: Dict[str, int] = {}
        for line in group.splitlines():
            for item in set(line):
                if counter.get(item) is None:
                    counter[item] = 0
                counter[item] += 1  # noqa
        for k, v in counter.items():
            if v == len(group.splitlines()):
                sum_ += 1
    return sum_


test_input_0 = """\
abc

a
b
c

ab
ac

a
a
a
a

b
"""

if __name__ == "__main__":
    assert part1(test_input_0) == 11
    print(part1(get_input()))
    print(part2(get_input()))
