"""AdventOfCode 2020 Day1"""


def find_sum(target=2020, numbers=set()):
    for n in numbers:
        second = target - n
        if second in numbers:
            return n * second
    raise ValueError("Not solvable")


def part1(target=2020, numbers=[]):
    return find_sum(target=target, numbers=set(numbers))


def part2(target=2020, numbers=[]):
    numbers = set(numbers)
    while numbers:
        selected = numbers.pop()
        remainer = 2020 - selected
        try:
            return selected * find_sum(numbers=numbers, target=remainer)
        except ValueError:
            continue


def get_input():
    with open('input/day1.txt') as f:
        numbers = [int(line) for line in f.read().splitlines()]
    return numbers


if __name__ == "__main__":
    print(part1(2020, get_input()))
    print(part2(2020, get_input()))
