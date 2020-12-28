"""AdventOfCode 2020 Day4."""
import re
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
    """Check passport is valid or not."""
    return all_ >= passport.keys() >= required


def valid_byr(passport: PassportData) -> bool:
    """Check if byr valid."""
    byr = passport.get("byr", 0)
    return 2002 >= int(byr) >= 1920


def valid_iyr(passport: PassportData) -> bool:
    """Check if iyr valid."""
    iyr = passport.get("iyr", 0)
    return 2020 >= int(iyr) >= 2010


def valid_eyr(passport: PassportData) -> bool:
    """Check if eyr valid."""
    eyr = passport.get("eyr", 0)
    return 2020 <= int(eyr) <= 2030


def valid_hgt(passport: PassportData) -> bool:
    """Check if hgt valid."""
    hgt = passport.get("hgt", "")
    if "cm" in hgt:
        cm = int(hgt.replace("cm", ""))
        return 150 <= cm <= 193
    elif "in" in hgt:
        in_ = int(hgt.replace("in", ""))
        return 59 <= in_ <= 76
    return False


def valid_hcl(passport: PassportData) -> bool:
    """Check if hcl valid."""
    return re.match(r"^\#[0-9a-f]{6}$", passport.get("hcl", "")) is not None


def valid_ecl(passport: PassportData) -> bool:
    """Check if ecl valid."""
    return passport.get("ecl", "") in [
        "amb",
        "blu",
        "brn",
        "gry",
        "grn",
        "hzl",
        "oth",
    ]  # noqa


def valid_pid(passport: PassportData) -> bool:
    """Check if pid valid."""
    return re.match(r"^[0-9]{9}$", passport.get("pid", "")) is not None


def valid_fields(passport: PassportData) -> bool:
    """If all valid function pass."""
    valid_funcs = [
        valid_byr,
        valid_iyr,
        valid_eyr,
        valid_hgt,
        valid_hcl,
        valid_ecl,
        valid_pid,
        valid_passport,
    ]
    return all(f(passport) for f in valid_funcs)


def part1(passports_str: str):
    """Part1."""
    return sum(1 for _ in filter(valid_passport, preprocess(passports_str)))


def part2(passports_str: str):
    """Part2."""
    return sum(valid_fields(passport) for passport in preprocess(passports_str))  # noqa


testvalid = """\
pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
"""

testinvalid = """\
eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007
"""


if __name__ == "__main__":
    print(part1(get_input()))
    print(part2(testvalid))
    print(part2(testinvalid))
    print(part2(get_input()))
