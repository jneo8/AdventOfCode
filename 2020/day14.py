"""AdventOfCode 2020 day14."""
from typing import Dict

test_input_1 = """\
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
"""


def get_input() -> str:
    """Get input str."""
    with open("input/day14.txt") as f:
        return f.read()


def write(memory, mask, address, value):
    """Write."""
    if "X" in mask:
        i = mask.index("X")
        # fmt: off
        write(memory, mask[:i] + "0" + mask[i + 1:], address, value)
        write(memory, mask[:i] + "1" + mask[i + 1:], address, value)
        # fmt: on
    else:
        memory[int(mask, 2) | address] = value


def part2(input_str: str) -> int:
    """Part1."""
    mask = ""
    m: Dict[int, int] = {}
    for line in input_str.strip().split("\n"):
        k, v = line.strip().split(" = ")
        if k == "mask":
            mask = v
        else:
            address = int(k[4:-1])
            value = int(v)
            address &= int(mask.replace("0", "1").replace("X", "0"), 2)
            write(m, mask, address, value)
    return sum(m.values())


def part1(input_str: str) -> int:
    """Part1."""
    mask = ""
    m: Dict[int, int] = {}
    for line in input_str.strip().split("\n"):
        k, v = line.strip().split(" = ")
        if k == "mask":
            mask = v
        else:
            address = int(k[4:-1])
            value = int(v)
            # fmt: off
            m[address] = (
                value
                & int(mask.replace("1", "0").replace("X", "1"), 2)
                | int(mask.replace("X", "0"), 2)
            )
            # fmt: on

    return sum(m.values())


if __name__ == "__main__":
    assert part1(test_input_1) == 165
    print(f"Part1: {part1(get_input())}")
    print(f"Part2: {part2(get_input())}")
