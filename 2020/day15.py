"""AdventOfCode Day15."""
from typing import Dict, List
from collections import defaultdict

test_input_1 = """1,3,2"""
test_input_2 = """2,1,3"""
puzzle_input = """18,11,9,0,5,1"""


def part1(input_str: str, target: int):
    """Part1."""
    map: Dict[int, List[int]] = defaultdict(list)

    numbers = [int(i) for i in input_str.strip().split(",")]
    for i, n in enumerate(numbers):
        map[n].append(i + 1)
    last = numbers[-1]

    for i in range(len(numbers) + 1, target + 1):
        if len(map[last]) < 2:
            map[0].append(i)
            last = 0
        else:
            last = map[last][-1] - map[last][-2]
            map[last].append(i)
            map[last] = map[last][-2:]
    return last


if __name__ == "__main__":
    assert part1(test_input_1, 2020) == 1
    assert part1(test_input_2, 2020) == 10
    print(f"Part1: {part1(puzzle_input, 2020)}")
    print(f"Part2: {part1(puzzle_input, 30000000)}")
