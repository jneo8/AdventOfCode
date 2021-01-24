"""AdventOfCode 2020 day13."""
from typing import List, Tuple
from functools import reduce

test_input_1 = """\
939
7,13,x,x,59,x,31,19
"""

test_input_2 = """\
0
17,x,13,19
"""

test_input_3 = """\
0
67,7,59,61
"""


def get_input() -> str:
    """Get input str."""
    with open("input/day13.txt") as f:
        return f.read()


def preprocess_input(input_str: str) -> Tuple[int, List[int]]:
    """Preprocess input."""
    inputs = input_str.strip().split("\n")
    return int(inputs[0]), [
        int(i.strip()) for i in map(str.strip, inputs[1].split(",")) if i != "x"  # noqa
    ]  # noqa


def chinese_remainder_theorem(mods: List[List[int]]) -> int:
    """https://en.wikipedia.org/wiki/Chinese_remainder_theorem ."""
    prod = reduce((lambda x, y: x * y), [i[0] for i in mods])
    sum = 0
    for n, remainder in mods:
        p = prod // n
        sum += remainder * mul_inv(p, n) * p
    return sum % prod


def mul_inv(a, b):
    """mul_inv."""
    b0 = b
    x0, x1 = 0, 1
    if b == 1:
        return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += b0
    return x1


def part1(input_str: str):
    """Part1."""
    earliestTimestamp, buses = preprocess_input(input_str)
    earliestBusTimestamp, earliestBus = min(
        [((earliestTimestamp // bus) * bus + bus, bus) for bus in buses]
    )
    return (earliestBusTimestamp - earliestTimestamp) * earliestBus


def part2(input_str: str):
    """Part2."""
    buses_with_mins = []
    buses = map(str.strip, input_str.strip().split("\n")[1].split(","))
    for i, bus in enumerate(buses):
        if bus.strip() != "x":
            b = int(bus)
            buses_with_mins.append([b, (b - i) % b])
    result = chinese_remainder_theorem(buses_with_mins)
    return result


if __name__ == "__main__":
    assert part1(test_input_1) == 295
    print(f"Part1: {part1(get_input())}")
    assert chinese_remainder_theorem([[3, 2], [5, 3], [7, 2]]) == 23
    assert chinese_remainder_theorem([[13, 11], [17, 0], [19, 16]]) == 3417
    assert part2(test_input_1) == 1068781
    assert part2(test_input_2) == 3417
    assert part2(test_input_3) == 754018
    print(f"Part2: {part2(get_input())}")
