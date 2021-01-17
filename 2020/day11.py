"""AdventOfCode 2020 Day11."""

from typing import List
import copy

EMPTY_SITE = "L"
OCCUPIED_SITE = "#"


test_input_1 = """\
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
"""

test_input_3 = """\
#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##
"""


def get_input() -> str:
    """Get input str."""
    with open("input/day11.txt") as f:
        return f.read()


def count_sites(sites: List[List[str]], site: str) -> int:
    c = 0
    for y_sites in sites:
        for x in y_sites:
            if x == site:
                c += 1
    return c


def get_adjacent_sites(
    first: bool, x: int, y: int, sites: List[List[str]]
) -> List[str]:
    site_idxs = [
        [-1, 0],
        [-1, +1],
        [-1, -1],
        [1, 0],
        [1, 1],
        [1, -1],
        [0, -1],
        [0, +1],
    ]
    adjacent_sites: List[str] = []

    if not first:
        for site_idx in site_idxs:
            if 0 <= x + site_idx[0] < len(sites[0]) and 0 <= y + site_idx[1] < len(
                sites
            ):  # noqa
                adjacent_sites.append(sites[y + site_idx[1]][x + site_idx[0]])
    else:
        for site_idx in site_idxs:
            adjacent_x = x + site_idx[0]
            adjacent_y = y + site_idx[1]
            while (
                len(sites[0]) > adjacent_x >= 0 and len(sites) > adjacent_y >= 0  # noqa
            ):  # noqa
                if sites[adjacent_y][adjacent_x] in [EMPTY_SITE, OCCUPIED_SITE]:  # noqa
                    adjacent_sites.append(sites[adjacent_y][adjacent_x])
                    break
                adjacent_x += site_idx[0]
                adjacent_y += site_idx[1]
    return adjacent_sites


def get_first_adjacent_sites(x: int, y: int, sites: List[List[str]]) -> List[str]:
    site_idxs = [
        [x - 1, y],
        [x - 1, y + 1],
        [x - 1, y - 1],
        [x + 1, y],
        [x + 1, y + 1],
        [x + 1, y - 1],
        [x, y - 1],
        [x, y + 1],
    ]
    adjacent_sites: List[str] = []

    for site_idx in site_idxs:
        if 0 <= site_idx[0] < len(sites[0]) and 0 <= site_idx[1] < len(sites):  # noqa
            adjacent_sites.append(sites[site_idx[1]][site_idx[0]])
    return adjacent_sites


def part1(input_str: str):
    sites = [list(line) for line in input_str.strip().split("\n")]
    return count_sites(arrive(sites, 4, False), OCCUPIED_SITE)


def part2(input_str: str):
    sites = [list(line) for line in input_str.strip().split("\n")]
    return count_sites(arrive(sites, 5, True), OCCUPIED_SITE)


def arrive(
    sites: List[List[str]], occupied_site_num: int, first_adjacent: bool
) -> List[List[str]]:
    new_sites = copy.deepcopy(sites)
    for idx_y, y in enumerate(sites):
        for idx_x, x in enumerate(y):
            if x == EMPTY_SITE and not any(
                site == OCCUPIED_SITE
                for site in get_adjacent_sites(
                    first_adjacent, idx_x, idx_y, sites
                )  # noqa
            ):  # noqa
                new_sites[idx_y][idx_x] = OCCUPIED_SITE
            elif (
                x == OCCUPIED_SITE
                and len(
                    [
                        site
                        for site in get_adjacent_sites(
                            first_adjacent, idx_x, idx_y, sites
                        )  # noqa
                        if site == OCCUPIED_SITE
                    ]
                )
                >= occupied_site_num
            ):  # noqa
                new_sites[idx_y][idx_x] = EMPTY_SITE

    if new_sites == sites:
        return new_sites
    return arrive(new_sites, occupied_site_num, first_adjacent)


if __name__ == "__main__":
    assert part1(test_input_1) == 37
    print(f"Part1: {part1(get_input())}")
    assert part2(test_input_1) == 26
    print(f"Part2: {part2(get_input())}")
