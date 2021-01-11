"""AdventOfCode 2020 Day8."""
import re
from typing import Set, List, Tuple

test_input_0 = """\
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""


line_re_obj = re.compile(
    r"(?P<operation>(nop|acc|jmp)) (?P<argument>(\+|\-)[\d]+)"
)  # noqa


def get_input() -> str:
    """Get input as str."""
    with open("input/day8.txt") as f:
        return f.read()


def get_instructions(input_str: str) -> List:
    """Get instructions list from input str."""
    instructions = []
    for line in input_str.splitlines():
        m = re.search(line_re_obj, line)
        if m is not None:
            instructions.append([m["operation"], int(m["argument"])])
    return instructions


def move(lines, part_1=False):
    seen = set()
    accumulator = 0
    idx = 0
    while True:
        if idx >= len(lines):
            return accumulator
        move, arg = lines[idx]
        if idx in seen:
            return accumulator if part_1 else False
        seen.add(idx)
        if move == "nop":
            idx += 1
        elif move == "acc":
            accumulator += arg
            idx += 1
        elif move == "jmp":
            idx += arg


def flip(val):
    return "jmp" if val == "nop" else "nop"


def change_piece(lines):
    for idx, turn in enumerate(lines):
        if turn[0] == "nop" or turn[0] == "jmp":
            prev = turn[0]
            lines[idx][0] = flip(turn[0])
            if accumulator := move(lines):
                return accumulator
            lines[idx][0] = prev


def part1(input_str=str):
    return move(get_instructions(input_str), True)


def part2(input_str=str):
    return change_piece(get_instructions(input_str))


if __name__ == "__main__":
    assert part1(test_input_0) == 5
    print(part1(get_input()))
    assert part2(test_input_0) == 8
    print(part2(get_input()))
