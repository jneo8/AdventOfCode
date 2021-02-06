"""AdventOfCode Day16."""

import re
import sys
from functools import reduce


def is_valid_field(i, rules):
    return any([v[0] <= i <= v[1] or v[2] <= i <= v[3] for v in rules.values()])


def product(array):
    return reduce((lambda x, y: x * y), array)


with open("input/day16.txt") as f:
    puzin = f.read().strip()

rules_raw, myticket_raw, others_raw = [x.split("\n") for x in puzin.split("\n\n")]

rules = {}
for rule in rules_raw:
    search = re.match(r"(.+): (\d+)-(\d+) or (\d+)-(\d+)", rule)
    name = search.group(1)
    nums = list(map(int, search.groups()[1:]))
    rules[name] = nums

others = [list(map(int, o.split(","))) for o in others_raw[1:]]
myticket = list(map(int, myticket_raw[1].split(",")))

ticket_scanning_error_rate = sum(
    [o for other in others for o in other if not is_valid_field(o, rules)]
)
print(f"Part 1: {ticket_scanning_error_rate}")


valid_others = [
    other for other in others if all([is_valid_field(o, rules) for o in other])
]


possibles = {}
for name, bounds in rules.items():
    possibles[name] = [
        i
        for i in range(len(rules))
        if all([is_valid_field(t[i], {name: bounds}) for t in valid_others])
    ]

matched = {}

for name, possibilities in sorted(possibles.items(), key=lambda x: len(x[1])):
    index = [i for i in possibilities if i not in matched]
    assert len(index) == 1
    matched[index[0]] = name

dep_prod = product([x for i, x in enumerate(myticket) if "departure" in matched[i]])
print(f"Part 2: {dep_prod}")
