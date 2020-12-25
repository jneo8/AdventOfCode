"""AdventOfCode 2020 Day3."""
from itertools import count, islice
from functools import reduce
from operator import mul


def get_input():
    """Get input as arr of arr str."""
    lines = []
    with open("input/day3.txt") as f:
        for line in f.read().splitlines():
            lines.append(list(line))
    return lines


def part1(trees, right=3, down=1):
    """Part 1."""
    rows = islice(
        trees, None, None, down
    )  # [tree[0], tree[0 + down], tree[0 + down * 2]]
    cols = count(step=right)  # [0, 0 + right, 0 + right * 2]

    return sum(row[col % len(row)] == "#" for (row, col) in zip(rows, cols))


def part2(trees):
    """Part 2."""
    counts = (
        part1(trees, r, d)
        for r, d in [
            (1, 1),
            (3, 1),
            (5, 1),
            (7, 1),
            (1, 2),
        ]
    )
    return reduce(mul, counts)


if __name__ == "__main__":
    print(part1(get_input()))
    print(part2(get_input()))
