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


def move(cups, moves, pad):
    nex = [i + 1 for i in range(pad + 1)]
    for i, label in enumerate(cups[:-1]):
        nex[label] = cups[i + 1]
    head = cups[0]
    if pad > len(cups):
        nex[-1] = head
        nex[cups[-1]] = max(cups) + 1
    else:
        nex[cups[-1]] = head

    for i in range(moves):
        rem = nex[head]
        nex[head] = nex[nex[nex[rem]]]
        allrem = rem, nex[rem], nex[nex[rem]]

        dest = head - 1 if head > 1 else pad
        while dest in allrem:
            dest = pad if dest == 1 else dest - 1

        nex[nex[nex[rem]]] = nex[dest]
        nex[dest] = rem

        head = nex[head]

    cup = nex[1]
    while cup != 1:
        yield cup
        cup = nex[cup]


def part1(puzzle_input: str, move: int):
    """Part1."""
    cups = playing([int(n) for n in list(puzzle_input)], move)
    idx_1 = cups.index(1)
    cups = cups[idx_1 + 1 :] + cups[:idx_1]  # noqa
    return "".join(str(n) for n in cups)


def part2(puzzle_input: str):
    """Part2."""
    cups = list(map(int, puzzle_input))
    m = move(cups, 10000000, 1000000)
    return next(m) * next(m)


if __name__ == "__main__":
    assert part1(test_input_1, 10) == "92658374"
    print(f"Part1: {part1(puzzle_input, 100)}")
    assert part2("389125467") == 149245887792
    print(f"Part2: {part2(puzzle_input)}")
