"""AdventOfCode Day18."""
import re

test_input_1 = """1 + 2 * 3 + 4 * 5 + 6"""
test_input_2 = """1 + (2 * 3) + (4 * (5 + 6))"""
test_input_3 = """5 + (8 * 3 + 9 + 3 * 4 * 3)"""
test_input_4 = """5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"""
test_input_5 = """((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"""
test_input_6 = """2 * 3 + (4 * 5)"""

OPERATORS = ["*", "+"]


def get_input():
    """Get puzzle input."""
    with open("input/day18.txt") as f:
        return f.read()


def part1(input_str: str):
    """Part1."""
    lines = input_str.strip().split("\n")
    sum = 0
    for line in lines:
        sum += calculate(line, False)
    return sum


def part2(input_str: str):
    """Part1."""
    lines = input_str.strip().split("\n")
    sum = 0
    for line in lines:
        x = calculate(line, True)
        # print(f"result: {x} formula: {line}")
        sum += x
    return sum


def calculate(input_str: str, part2: bool):
    """Input formula string and return result."""
    s = input_str
    while True:
        formulas = re.findall(
            r"(?P<formula>\((?P<formula_without_brackets>[0-9\+\*\s]+)\))", s
        )
        if len(formulas) == 0:
            break
        for formula in formulas:
            formula_result = calculate(formula[1], part2)
            s = s.replace(formula[0], str(formula_result))

    if part2:
        while True:
            formulas = re.findall(r"(?P<formula>[0-9]+ \+ [0-9]+)", s)
            if len(formulas) == 0:
                break
            for formula in formulas:
                result = formula.split(" ")
                s = s.replace(formula, str(int(result[0]) + int(result[2])), 1)

    operator = ""
    sum = 0
    for idx, c in enumerate(s.strip().split(" ")):
        if idx == 0:
            sum += int(c)
            continue
        elif c in OPERATORS:
            operator = c  # noqa
        else:
            if operator == "+":
                sum = sum + int(c)
            else:
                sum = int(c) * sum
    return sum


if __name__ == "__main__":
    assert calculate(test_input_1, False) == 71
    assert calculate(test_input_2, False) == 51
    print(f"Part1: {part1(get_input())}")
    assert calculate(test_input_2, True) == 51
    assert calculate(test_input_3, True) == 1445
    assert calculate(test_input_4, True) == 669060
    assert calculate(test_input_5, True) == 23340
    assert calculate(test_input_6, True) == 46
    print(f"Part2: {part2(get_input())}")
