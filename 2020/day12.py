"""AdventOfCode 2020 Day12."""
import math

input_text_1 = """\
F10
N3
F7
R90
F11\
"""


FOUR_WAYS = "ESWN"


def get_input() -> str:
    """Get input str."""
    with open("input/day12.txt") as f:
        return f.read()


class Ship:
    """Ship."""

    facing = "E"
    x = 0
    y = 0
    wpx = 0
    wpy = 0

    def __init__(self, x, y, wpx, wpy: int = 0, facing: str = "E"):
        """__Init__."""
        self.x = x
        self.y = y
        self.facing = facing
        self.wpx = wpx
        self.wpy = wpy

    def rotate(self, angle):
        """Rotate."""
        qx = math.cos(angle) * self.wpx - math.sin(angle) * self.wpy
        qy = math.sin(angle) * self.wpx + math.cos(angle) * self.wpy
        self.wpx, self.wpy = int(round(qx)), int(round(qy))

    def move_wp(self, s: str):
        """Input action 2."""
        way, n = s[0], int(s[1:])
        if way == "N":
            self.wpy += n
        elif way == "S":
            self.wpy -= n
        elif way == "E":
            self.wpx += n
        elif way == "W":
            self.wpx -= n
        elif way == "F":
            self.x += self.wpx * n
            self.y += self.wpy * n
        elif way in ["R", "L"]:
            if way == "R":
                n = -n
            self.rotate(math.radians(n))

    def move(self, s: str):
        """Input action."""
        way, n = s[0], int(s[1:])
        if way == "L":
            self.facing = FOUR_WAYS[(FOUR_WAYS.find(self.facing) - n // 90) % 4]  # noqa
        elif way == "R":
            self.facing = FOUR_WAYS[(FOUR_WAYS.find(self.facing) + n // 90) % 4]  # noqa
        elif way == "N":
            self.y += n
        elif way == "S":
            self.y -= n
        elif way == "E":
            self.x += n
        elif way == "W":
            self.x -= n
        elif way == "F":
            self.move(self.facing + str(n))

    def __str__(self):
        """__str__."""
        return f"{self.x}, {self.y} {self.facing}"

    def get_manhattan_distance(self) -> int:
        """Return mahattan distance."""
        return abs(self.x) + abs(self.y)


def part1(input_str: str) -> int:
    """Part1."""
    ship = Ship(x=0, y=0, wpx=0, wpy=0, facing="E")
    for action in input_str.strip().split("\n"):
        ship.move(action)
    return ship.get_manhattan_distance()


def part2(input_str: str) -> int:
    """Part1."""
    ship = Ship(x=0, y=0, wpx=10, wpy=1, facing="E")
    for action in input_str.strip().split("\n"):
        ship.move_wp(action)
    return ship.get_manhattan_distance()


if __name__ == "__main__":
    assert part1(input_text_1) == 25
    print(f"Part1: {part1(get_input())}")
    assert part2(input_text_1) == 286
    print(f"Part2: {part2(get_input())}")
