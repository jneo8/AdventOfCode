"""AdventOfCode Day17."""
import copy
import itertools

ACTIVE = "#"
INACTIVE = "."


test_input_0 = """
.#.
..#
###
"""


def get_input():
    with open("input/day17.txt") as f:
        return f.read()


def preprocess(input_str: str):
    """Split input str into list."""
    return [list(row) for row in input_str.strip().splitlines()]


def part1(input_str: str) -> int:
    """Part1."""
    data = preprocess(input_str)

    rows = len(data)
    columns = len(data[0])
    loops = 6
    expanded = loops * 2

    # fmt: off
    grid = [
        [
            [INACTIVE for _ in range(columns + expanded)]
            for _ in range(rows + expanded)
        ]
        for _ in range(1 + expanded)
    ]
    # fmt: on

    for ix, i in enumerate(data):
        for jx, j in enumerate(i):
            grid[loops][ix + loops][jx + loops] = j

    si = sj = sk = loops - 1

    for loop in range(loops):
        grid_clone = copy.deepcopy(grid)

        range_expanded = 2 * (loop + 1)
        for i in range(1 + range_expanded):
            for j in range(rows + range_expanded):
                for k in range(columns + range_expanded):
                    count_active = 0
                    idx_x = i + si
                    idx_y = j + sj
                    idx_z = k + sk
                    for z in itertools.product([0, 1, -1], repeat=3):
                        if (
                            not (z == (0, 0, 0))
                            and (0 <= idx_x + z[0] < 1 + expanded)
                            and (0 <= idx_y + z[1] < rows + expanded)
                            and (0 <= idx_z + z[2] < columns + expanded)
                            and (
                                grid[idx_x + z[0]][idx_y + z[1]][idx_z + z[2]]
                                == ACTIVE  # noqa
                            )
                        ):
                            count_active += 1

                    if (grid[idx_x][idx_y][idx_z] == ACTIVE) and (
                        not (2 <= count_active <= 3)
                    ):
                        grid_clone[idx_x][idx_y][idx_z] = INACTIVE

                    if (grid[idx_x][idx_y][idx_z] == INACTIVE) and (
                        count_active == 3
                    ):  # noqa
                        grid_clone[idx_x][idx_y][idx_z] = ACTIVE
        grid = grid_clone
        si, sj, sk = si - 1, sj - 1, sk - 1

    active = 0
    for i in range(1 + expanded):
        for j in range(rows + expanded):
            for k in range(columns + expanded):
                if grid[i][j][k] == ACTIVE:
                    active += 1
    return active


def part2(input_str: str):
    data = preprocess(input_str)
    rows = len(data)
    columns = len(data[0])
    loops = 6
    expanded = loops * 2

    grid = [
        [
            [
                [INACTIVE for _ in range(columns + expanded)]
                for _ in range(rows + expanded)
            ]
            for _ in range(1 + expanded)
        ]
        for _ in range(1 + expanded)
    ]
    for ix, i in enumerate(data):
        for jx, j in enumerate(i):
            grid[loops][loops][ix + loops][jx + loops] = j

    si = sj = sk = sl = loops - 1

    for loop in range(loops):
        grid_clone = copy.deepcopy(grid)

        range_expanded = 2 * (loop + 1)
        for i in range(1 + range_expanded):
            for j in range(1 + range_expanded):
                for k in range(rows + range_expanded):
                    for l in range(columns + range_expanded):
                        count_active = 0
                        for z in itertools.product([0, 1, -1], repeat=4):
                            if (
                                not (z == (0, 0, 0, 0))
                                and (0 <= i + si + z[0] < 1 + expanded)
                                and (0 <= j + sj + z[1] < 1 + expanded)
                                and (0 <= k + sk + z[2] < rows + expanded)
                                and (0 <= l + sl + z[3] < columns + expanded)
                                and (
                                    grid[i + si + z[0]][j + sj + z[1]][k + sk + z[2]][
                                        l + sl + z[3]
                                    ]
                                    == ACTIVE
                                )
                            ):
                                count_active += 1

                        if (grid[i + si][j + sj][k + sk][l + sl] == ACTIVE) and (
                            not (2 <= count_active <= 3)
                        ):
                            grid_clone[i + si][j + sj][k + sk][l + sl] = INACTIVE

                        if (grid[i + si][j + sj][k + sk][l + sl] == INACTIVE) and (
                            count_active == 3
                        ):
                            grid_clone[i + si][j + sj][k + sk][l + sl] = ACTIVE
        grid = grid_clone
        si, sj, sk, sl = si - 1, sj - 1, sk - 1, sl - 1

    # Count active cubes
    active = 0
    for i in range(1 + expanded):
        for j in range(1 + expanded):
            for k in range(rows + expanded):
                for l in range(columns + expanded):
                    if grid[i][j][k][l] == ACTIVE:
                        active += 1
    return active


if __name__ == "__main__":
    print(part1(test_input_0))
    print(part1(get_input()))
    print(part2(get_input()))
