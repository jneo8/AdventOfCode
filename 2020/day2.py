"""AdventOfCode 2020 Day2."""
import re
from dataclasses import dataclass

line_re_obj = re.compile(
    r"^(?P<min>\d+)-(?P<max>\d+) (?P<target>[a-z]): (?P<pwd>[a-z]+)$"
)  # noqa


@dataclass
class PWD:
    """Cls for PWD check."""

    min_: int
    max_: int
    letter: str
    password: str

    @classmethod
    def from_line(cls, line: str) -> "PWD":
        """Return PWD from line."""
        match = line_re_obj.search(line)

        if match is not None:
            min_ = int(match["min"])
            max_ = int(match["max"])
            return cls(min_, max_, match["target"], match["pwd"])
        else:
            raise ValueError("line regexp not match")

    def is_valid(self) -> bool:
        """Is valid."""
        return self.min_ <= self.password.count(self.letter) <= self.max_


def get_input():
    """Get input as string array."""
    with open("input/day2.txt") as f:
        lines = [line for line in f.read().splitlines()]  # noqa
    return lines


def part1(lines) -> int:
    """Part1."""
    return sum([PWD.from_line(line).is_valid() for line in lines])


if __name__ == "__main__":
    print(part1(get_input()))
