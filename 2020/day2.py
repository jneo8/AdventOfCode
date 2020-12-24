"""AdventOfCode 2020 Day2."""
import re
from dataclasses import dataclass

line_re_obj = re.compile(
    r"^(?P<n1>\d+)-(?P<n2>\d+) (?P<target>[a-z]): (?P<pwd>[a-z]+)$"
)  # noqa


@dataclass
class PWD:
    """Cls for PWD check."""

    n1: int
    n2: int
    target: str
    password: str

    @classmethod
    def from_line(cls, line: str) -> "PWD":
        """Return PWD from line."""
        match = line_re_obj.search(line)

        if match is not None:
            n1 = int(match["n1"])
            n2 = int(match["n2"])
            return cls(n1, n2, match["target"], match["pwd"])
        else:
            raise ValueError("line regexp not match")

    def rule1_is_valid(self) -> bool:
        """Is valid:  n2 >= target count >= n1."""
        return self.n1 <= self.password.count(self.target) <= self.n2

    def rule2_is_valid(self) -> bool:
        """Is valid: n1 == target & n2 != target."""
        return (
            self.password[self.n1 - 1],
            self.password[self.n2 - 1],
        ).count(self.target) == 1


def get_input():
    """Get input as string array."""
    with open("input/day2.txt") as f:
        lines = [line for line in f.read().splitlines()]  # noqa
    return lines


def part1(lines) -> int:
    """Part 1."""
    return sum([PWD.from_line(line).rule1_is_valid() for line in lines])


def part2(lines) -> int:
    """Part 2."""
    return sum([PWD.from_line(line).rule2_is_valid() for line in lines])


if __name__ == "__main__":
    print(part1(get_input()))
    print(part2(get_input()))
