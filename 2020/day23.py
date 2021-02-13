"""AdventOfCode 2020 Day23."""
from typing import List
import collections

test_input_1 = "389125467"
puzzle_input = "925176834"


def playing(cups: List[int], move: int):
    """Playing."""
    max_cup = max(cups)
    min_cup = min(cups)
    q = collections.deque(cups, maxlen=len(cups))

    for round in range(1, move + 1):
        current_cup = q.popleft()
        pickup_cups = []
        for pickup in range(0, 3):
            pickup_cups.append(q.popleft())

        distination_cup = current_cup - 1
        if distination_cup < min_cup:
            distination_cup = max_cup
        while distination_cup in pickup_cups:
            distination_cup -= 1
            if distination_cup < min_cup:
                distination_cup = max_cup

        distination_cup_idx = q.index(distination_cup)
        for idx, cup in enumerate(pickup_cups):
            q.insert(distination_cup_idx + 1 + idx, cup)
        q.append(current_cup)
    return list(q)


def part1(puzzle_input: str, move: int):
    """Part1."""
    cups = playing([int(n) for n in list(puzzle_input)], move)
    idx_1 = cups.index(1)
    cups = cups[idx_1 + 1 :] + cups[:idx_1]  # noqa
    return "".join(str(n) for n in cups)


if __name__ == "__main__":
    assert part1(test_input_1, 10) == "92658374"
    print(f"Part1: {part1(puzzle_input, 100)}")
