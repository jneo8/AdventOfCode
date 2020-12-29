"""AdventOfCode 2020 Day5."""


def get_input() -> str:
    """Get input as str."""
    with open("input/day5.txt") as f:
        return f.read()


def get_seat(max_: int, min_: int, upper_or_lower: list):
    """Recusive get seat."""
    if len(upper_or_lower) == 0:
        return max_

    upper_or_lower_character = upper_or_lower.pop(0)
    mid = int((max_ + min_) / 2)
    if upper_or_lower_character in "FL":
        return get_seat(
            max_=mid,
            min_=min_,
            upper_or_lower=upper_or_lower,
        )
    # Else
    return get_seat(
        max_,
        mid + 1,
        upper_or_lower,
    )


def get_seat_id(input_str: str) -> int:
    """Get seat id."""
    row = get_seat(127, 0, list(input_str)[:7])
    column = get_seat(7, 0, list(input_str)[7:])
    return row * 8 + column


def part1(input_str: str):
    """Part1."""
    return max(get_seat_id(line) for line in input_str.splitlines())


def part2(input_str: str):
    """Part2."""
    seat_ids = [get_seat_id(line) for line in input_str.splitlines()]
    seat_ids.sort()
    for i in range(len(seat_ids)):
        if seat_ids[i + 1] - seat_ids[i] != 1:
            return seat_ids[i] + 1


test_input_0 = "FBFBBFFRLR"
test_input_1 = "BFFFBBFRRR"
test_input_2 = "FFFBBBFRRR"
test_input_3 = "BBFFBBFRLL"


if __name__ == "__main__":
    assert get_seat_id(test_input_0) == 357
    assert get_seat_id(test_input_1) == 567
    assert get_seat_id(test_input_2) == 119
    assert get_seat_id(test_input_3) == 820
    print(part1(get_input()))
    print(part2(get_input()))
