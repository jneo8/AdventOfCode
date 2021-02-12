"""AdventOfCode 2020 Day20."""
import re
import math
import itertools

TOP, BOTTOM, LEFT, RIGHT = range(4)

MONSTER = [
    "..................#.",
    "#....##....##....###",
    ".#..#..#..#..#..#...",
]


test_input_1 = """\
Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...\
"""


def get_input():
    """Get puzzle input."""
    with open("input/day20.txt") as f:
        return f.read()


class Tile:
    """Tile."""

    def __init__(self, raw_str):
        """__Init__."""
        name, *grid = raw_str.splitlines()
        self.id = int(re.search(r"\d+", name).group(0))
        self.inner = [line[1:-1] for line in grid[1:-1]]
        self.neighbours = set()

        top, bottom = grid[0], grid[-1]
        left = "".join(row[0] for row in grid)
        rigth = "".join(row[-1] for row in grid)
        self.edges = [top, bottom, left, rigth]
        self.edge_combinations = set(self.edges + [e[::-1] for e in self.edges])  # noqa
        self.rotation_count = 0
        self.flipped = False

    def __hash__(self):
        """__hash__."""
        return self.id

    def connect_check(self, other):
        """Check if tile conn."""
        for edge in self.edges:
            if edge in other.edge_combinations:
                self.neighbours.add(other)
                other.neighbours.add(self)
                return True
        return False

    def rotate(self):
        """Retate."""
        top, bottom, left, right = self.edges
        self.edges = [left[::-1], right[::-1], bottom, top]
        self.rotation_count += 1 % 4

    def flip(self):
        """Flip tile."""
        top, bottom, left, right = self.edges
        self.edges = [top[::-1], bottom[::-1], right, left]
        self.flipped = not self.flipped

    def aligned(self, other, own_edge, other_edge):
        """Aligned."""
        target_edge = other.edges[other_edge]
        if self._rotate_match(own_edge, target_edge):
            return True
        self.flip()
        if self._rotate_match(own_edge, target_edge):
            return True
        self.flip()
        return False

    def _rotate_match(self, own_edge, target_edge):
        for _ in range(4):
            if self.edges[own_edge] == target_edge:
                return True
            else:
                self.rotate()
        return False

    def _get_neighbour(self, disconnect, own_edge=RIGHT, other_edge=LEFT):
        for neighbour in self.neighbours:
            if neighbour.aligned(self, other_edge, own_edge):
                if disconnect:
                    neighbour.neighbours.discard(self)
                    self.neighbours.discard(neighbour)
                return neighbour
        return None

    def right_neighbour(self, disconnect=True):
        """Get right neighbour."""
        return self._get_neighbour(disconnect)

    def below_neighbour(self, disconnect=True):
        """Get below neighbour."""
        return self._get_neighbour(disconnect, BOTTOM, TOP)

    def align_inner(self):
        """Get inner."""
        if self.flipped:
            self.inner = flip(self.inner)
        for _ in range(self.rotation_count):
            self.inner = rotate(self.inner)
        return self.inner


def preprocess(puzzle_input: str):
    """Preprocess."""
    tiles = puzzle_input.split("\n\n")
    tile_map = {}
    for tile in tiles:
        id = int(tile.split(":")[0].replace("Tile ", ""))
        tile_map[id] = tile.split(":")[1].strip().split("\n")
    return tile_map


def flip(grid):
    return tuple(row[::-1] for row in grid)


def rotate(grid):
    return tuple("".join(c[::-1]) for c in zip(*grid))


MONSTER_RE1 = re.compile(f"(?=({MONSTER[2]}))")
MONSTER_RE2 = re.compile(MONSTER[1])
MONSTER_RE3 = re.compile(MONSTER[0])


def count_monsters(img):
    count = 0
    for first, second, third in zip(img[:-2], img[1:-1], img[2:]):
        for match in MONSTER_RE1.finditer(first):
            # zero width match due to lookahead searching
            start = match.span()[0]
            end = start + 20
            if MONSTER_RE2.match(second[start:end]) and MONSTER_RE3.match(
                third[start:end]
            ):
                count += 1
    return count


def top_left(corners):
    for corner in corners:
        for _ in range(4):
            corner.rotate()
            right = corner.right_neighbour(disconnect=False)
            below = corner.below_neighbour(disconnect=False)
            if right and below:
                return corner


def get_corners(puzzle_input: str):
    """Get corner tiles."""
    tiles = tuple(map(Tile, puzzle_input.strip().split("\n\n")))
    for tile_a, tile_b in itertools.combinations(tiles, 2):
        tile_a.connect_check(tile_b)
    corners = filter(lambda t: len(t.neighbours) == 2, tiles)
    return corners


def part1(puzzle_input: str):
    """Part1."""
    return math.prod(tile.id for tile in get_corners(puzzle_input))


def part2(puzzle_input: str):
    """Part2."""
    corners = get_corners(puzzle_input)

    tile = top_left(corners)

    aligned = []
    while True:
        row = [tile]
        while True:
            if not (tile := tile.right_neighbour()):
                break
            row.append(tile)
        aligned.append(row)
        if not (tile := row[0].below_neighbour()):
            break

    image = []
    for row in aligned:
        inner_row = tuple(tile.align_inner() for tile in row)
        image.extend(map("".join, zip(*inner_row)))

    for rotation in range(8):
        if monster_count := count_monsters(image):
            water = sum(row.count("#") for row in image)
            monster = sum(row.count("#") for row in MONSTER)
            return water - monster * monster_count
        if rotation == 4:
            image = flip(image)
        else:
            image = rotate(image)

    return 0


if __name__ == "__main__":
    assert part1(test_input_1) == 20899048083289
    print(f"Part1: {part1(get_input())}")
    assert part2(test_input_1) == 273
    print(f"Part2: {part2(get_input())}")
