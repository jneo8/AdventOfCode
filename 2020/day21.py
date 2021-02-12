"""AdventOfCode 2020 Day21."""
import re
import collections
import z3

test_input_1 = """\
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)\
"""


def get_input():
    """Get puzzle input."""
    with open("input/day21.txt") as f:
        return f.read()


def preprocess(pazzle_input: str):
    line_regexp = r"(?P<ingredients>.*) \(contains (?P<allergens>.*)\)"
    allwhere = collections.defaultdict(set)
    ingwhere = collections.defaultdict(set)

    for i, line in enumerate(pazzle_input.strip().splitlines()):
        match_obj = re.fullmatch(line_regexp, line)
        if match_obj:
            ingredients = match_obj.groups()[0].split(" ")
            allergens = match_obj.groups()[1].replace(" ", "").split(",")
            for ing in ingredients:
                ingwhere[ing].add(i)
            for allergen in allergens:
                allwhere[allergen].add(i)
    return ingwhere, allwhere


def get_inert_and_cnt(ingwhere, allwhere):
    """Return inert set and cnt."""
    inert = set()
    cnt = 0
    for ingredient, ingredient_foods in ingwhere.items():
        canallerg = False
        for allergen, allergen_vals in allwhere.items():
            if allergen_vals < ingredient_foods:
                canallerg = True
        if not canallerg:
            inert.add(ingredient)
            cnt += len(ingwhere[ingredient])
    return cnt, inert


def part1(pazzle_input: str):
    """Part1."""
    ingwhere, allwhere = preprocess(pazzle_input)
    cnt, _ = get_inert_and_cnt(ingwhere, allwhere)
    return cnt


def part2(pazzle_input: str):
    """Part2."""
    ingwhere, allwhere = preprocess(pazzle_input)
    _, inert = get_inert_and_cnt(ingwhere, allwhere)

    poss_ingredient = list(set(ingwhere.keys()) - inert)
    poss_allergens = list(set(allwhere.keys()))

    assigments = z3.IntVector("allergen", len(poss_allergens))
    solver = z3.Solver()
    for a in assigments:
        solver.add(0 <= a)
        solver.add(a < len(poss_allergens))

    solver.add(z3.Distinct(assigments))

    for ai, allergen in enumerate(poss_allergens):
        conds = []
        for ii, ing in enumerate(poss_ingredient):
            if ingwhere[ing] >= allwhere[allergen]:
                conds.append(assigments[ii] == ai)
        solver.add(z3.Or(conds))

    assert solver.check() == z3.sat

    m = solver.model()
    matches = []
    for ii, a in enumerate(assigments):
        matches.append(
            (poss_allergens[m.evaluate(assigments[ii]).as_long()], poss_ingredient[ii])
        )
    matches.sort()
    return ",".join(m[1] for m in matches)


if __name__ == "__main__":
    assert part1(test_input_1) == 5
    print(f"Part1: {part1(get_input())}")
    assert part2(test_input_1) == "mxmxvkd,sqjhc,fvjkl"
    print(f"Part2: {part2(get_input())}")
