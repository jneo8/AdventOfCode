"""AdventOfCode 2020 Day7."""
import re


test_input_0 = """\
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
"""

test_input_1 = """\
shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.
"""


bag_re_obj = re.compile(
    r"(?P<n>[\d]+)?(\s)?(?P<bag>[a-zA-Z\s]+?) (bags|bag).(contain no other bags)?"  # noqa
)


def get_input() -> str:
    """Get input as str."""
    with open("input/day7.txt") as f:
        return f.read()


def get_bag(input_str: str):
    """Get bag parent and children."""
    m = re.findall(bag_re_obj, input_str)
    d = {}
    parent = m[0][2]
    for color in m[0:]:
        if color[0]:
            d[color[2]] = int(color[0])
    return parent, d


def get_bags(input_str: str):
    """Process input str to bags dict."""
    bags = {}
    for line in input_str.splitlines():
        k, dict_ = get_bag(line)
        bags[k] = dict_
    return bags


def include_bag(bags, k: str, want: str):
    """Check if bags k include want bag."""
    if len(bags[k]) == 0:
        return False
    elif bags[k].get(want) is not None:
        return True
    else:
        return any(include_bag(bags, children, want) for children in bags[k])
    return True


def get_bag_count(bags, k: str) -> int:
    return sum(bags[k].values()) + sum(
        [get_bag_count(bags, k) * v for k, v in bags[k].items()]
    )


def part1(input_str: str):
    """Part1."""
    bags = get_bags(input_str)
    return sum(include_bag(bags, bag, "shiny gold") for bag in bags)


def part2(input_str: str):
    """Part2."""
    bags = get_bags(input_str)
    return get_bag_count(bags, "shiny gold")


if __name__ == "__main__":
    assert part1(test_input_0) == 4
    assert part2(test_input_1) == 126
    print(part1(get_input()))
    print(part2(get_input()))
