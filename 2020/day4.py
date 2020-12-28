"""AdventOfCode 2020 Day4."""
from typing import Iterable, Mapping

PassportData = Mapping[str, str]

required = frozenset({"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"})
all_ = required | frozenset({"cid"})


def get_input():
    """Get inputs."""
    with open("input/day4.txt") as f:
        return f.read()


def preprocess(s: str) -> Iterable[PassportData]:
    """Preprocess for raw data."""
    for line in s.split("\n\n"):
        yield dict((f.split(":")[0], f.split(":")[1]) for f in line.split())


def valid_passport(passport: PassportData) -> bool:
    """Return passport is valid or not."""
    return all_ >= passport.keys() >= required


def part1(passports_str: str):
    """Part1."""
    return sum(1 for _ in filter(valid_passport, preprocess(passports_str)))


if __name__ == "__main__":
    print(part1(get_input()))
