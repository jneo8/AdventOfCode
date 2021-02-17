"""AdventOfCode 2020 Day25."""

test_input_1 = """
5764801
17807724
"""


def get_input():
    """Get puzzle input."""
    with open("input/day25.txt") as f:
        return f.read()


def get_loop_size(public_key: int, subject_number: int):
    """Get loop size with public_key and subject_number."""
    v = subject_number
    loop_size = 1
    while v != public_key:
        loop_size += 1
        v = v * subject_number % 20201227
    return loop_size


def part1(puzzle_input: str) -> int:
    """Part1."""
    input = puzzle_input.strip().splitlines()
    card_pub_key = int(input[0])
    door_pub_key = int(input[1])
    card_loop_size = get_loop_size(card_pub_key, 7)
    return pow(door_pub_key, card_loop_size, 20201227)


if __name__ == "__main__":
    assert get_loop_size(5764801, 7) == 8
    assert get_loop_size(17807724, 7) == 11
    assert (part1(test_input_1)) == 14897079
    print(f"Part1: {part1(get_input())}")
