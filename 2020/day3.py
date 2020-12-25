"""AdventOfCode 2020 Day3."""
from itertools import count, islice


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


if __name__ == "__main__":
    print(part1(get_input()))
