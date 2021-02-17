"""AdventOfCode 2020 Day24."""
from typing import List, Tuple, Dict
from collections import defaultdict


test_input_1 = """\
sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew\
"""

test_input_2 = """\
nwwswee
"""


def get_input():
    """Get puzzle input."""
    with open("input/day24.txt") as f:
        return f.read()


def move(previous: Tuple[int, int] = (0, 0), move: str = "") -> Tuple[int, int]:  # noqa
    """Move."""
    x = previous[0]
    y = previous[1]
    if move == "e":
        x += 2
    elif move == "w":
        x -= 2
    elif move == "ne":
        x += 1
        y += 1
    elif move == "se":
        x += 1
        y -= 1
    elif move == "nw":
        x -= 1
        y += 1
    elif move == "sw":
        x -= 1
        y -= 1
    return (x, y)


def preprocess(puzzle_input: str) -> List[List[str]]:
    """Transform puzzle input to tile list."""
    lines = [list(line) for line in puzzle_input.splitlines()]
    all_tiles = []
    for line in lines:
        tiles = []
        for s in line:
            if s in ["n", "s"]:
                tiles.append(s)
            else:
                if len(tiles) == 0 or tiles[-1] not in ["n", "s"]:
                    tiles.append(s)
                else:
                    tiles[-1] += s
        all_tiles.append(tiles)
    return all_tiles


def get_tiles(need_flip_tiles: List[List[str]]) -> Dict[Tuple[int, int], int]:
    """Flip tile with list of list flip."""
    tiles: Dict[Tuple[int, int], int] = {(0, 0): 0}

    for moves in need_flip_tiles:
        reference_tile = (0, 0)
        for idx, flip_tile in enumerate(moves):
            tile = move(previous=reference_tile, move=flip_tile)  # noqa
            reference_tile = tile
            # Last move
            if idx == len(moves) - 1:
                if tile not in tiles:
                    tiles[tile] = 1
                else:
                    tiles[tile] += 1
    return tiles


def get_neigbors(tile: Tuple[int, int]) -> List[Tuple[int, int]]:
    """Return tile's 6 neighbor coordinate."""
    return [
        (tile[0] + 2, tile[1]),  # e
        (tile[0] - 2, tile[1]),  # w
        (tile[0] + 1, tile[1] + 1),  # ne
        (tile[0] + 1, tile[1] - 1),  # se
        (tile[0] - 1, tile[1] + 1),  # nw
        (tile[0] - 1, tile[1] - 1),  # sw
    ]


def get_black_tiles(
    tiles: Dict[Tuple[int, int], int],
) -> List[Tuple[int, int]]:
    """Return black tiles."""
    return [t for t, c in tiles.items() if c % 2 == 1]


def part1(puzzle_input: str):
    """Part1."""
    need_flip_tiles = preprocess(puzzle_input)
    tiles = get_tiles(need_flip_tiles)
    return len(get_black_tiles(tiles))


def part2(puzzle_input: str, days: int = 100):
    """Part2."""
    need_flip_tiles = preprocess(puzzle_input)
    tiles = get_tiles(need_flip_tiles)
    black_tiles = get_black_tiles(tiles)

    for i in range(0, days):
        black_neighbor_cnt = defaultdict(int)

        for t in black_tiles:
            black_neighbor_cnt[t] = 0

        for tile in black_tiles:
            neighbors = get_neigbors(tile)
            for neighbor in neighbors:
                black_neighbor_cnt[neighbor] += 1

        flipped_tiles: List[Tuple[int, int]] = []
        for tile, neighbor_cnt in black_neighbor_cnt.items():
            if tile in black_tiles and neighbor_cnt in [1, 2]:
                # Still Black
                flipped_tiles.append(tile)
            if tile not in black_tiles and neighbor_cnt == 2:
                flipped_tiles.append(tile)
        black_tiles = flipped_tiles
    return len(black_tiles)


if __name__ == "__main__":
    assert part1(test_input_1) == 10
    print(f"Part1: {part1(get_input())}")
    assert part2(test_input_1) == 2208
    print(f"Part2: {part2(get_input())}")
