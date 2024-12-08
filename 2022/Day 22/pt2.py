import copy
import re

turn_dict = {
    ">": {"L": "^", "R": "v"},
    "<": {"L": "v", "R": "^"},
    "^": {"L": "<", "R": ">"},
    "v": {"L": ">", "R": "<"},
}

display_grid = []


def get_lines(filename: str):
    lines = []

    f = open(filename, "r")
    for line in f:
        lines.append(line.strip())

    f.close()
    return lines


# end_get_lines


def fill_grid(grid, max_len):
    start_x = 0

    for i in range(len(grid)):
        if i == 0:
            for x in range(len(grid[i])):
                if grid[i][x] == ".":
                    start_x = x
                    break
        while len(grid[i]) < max_len:
            grid[i].append(" ")

    return start_x


def get_quadrant(x: int, y: int) -> int:
    if (x >= 0 and x <= 49) and (y >= 150 and y <= 199):
        return 1
    elif (x >= 0 and x <= 49) and (y >= 100 and y <= 149):
        return 2
    elif (x >= 50 and x <= 99) and (y >= 100 and y <= 149):
        return 3
    elif (x >= 50 and x <= 99) and (y >= 50 and y <= 99):
        return 4
    elif (x >= 50 and x <= 99) and (y >= 0 and y <= 49):
        return 5
    elif (x >= 100 and x <= 149) and (y >= 0 and y <= 49):
        return 6
    return 0


def global_to_local_coords(x: int, y: int) -> tuple[int, int]:
    q = get_quadrant(x, y)

    if q == 1:
        y -= 150
    elif q == 2:
        y -= 100
    elif q == 3:
        x -= 50
        y -= 100
    elif q == 4:
        x -= 50
        y -= 50
    elif q == 5:
        x -= 50
    elif q == 6:
        x -= 100

    return (x, y)


def local_to_global_coords(x: int, y: int, q: int) -> tuple[int, int]:
    if q == 1:
        y += 150
    elif q == 2:
        y += 100
    elif q == 3:
        x += 50
        y += 100
    elif q == 4:
        x += 50
        y += 50
    elif q == 5:
        x += 50
    elif q == 6:
        x += 100

    return (x, y)


def step_boundary(grid: list[list[str]], pos: list[str | int]) -> list[str | int]:
    x, y, facing = pos
    x = int(x)
    y = int(y)
    q0 = get_quadrant(x, y)
    l_x, l_y = global_to_local_coords(x, y)

    if facing == ">":
        # right of 1 is bottom of 3 approaching upwards, use q1_y as q3_x
        if q0 == 1:
            l_x, l_y = local_to_global_coords(l_y, 0, 3)
            if grid[149][l_x] == ".":
                pos = [l_x, 149, "^"]

        # right of 3 is right of 6 approaching leftwards, use inverse q3_y as q6_y
        if q0 == 3:
            l_x, l_y = global_to_local_coords(x, y)
            if grid[49 - l_y][149] == ".":
                pos = [149, 49 - l_y, "<"]

        # right of 4 is bottom of 6 approaching upwards, use q4_y as q6_x
        if q0 == 4:
            l_x, l_y = local_to_global_coords(l_y, 0, 6)
            if grid[49][l_x] == ".":
                pos = [l_x, 49, "^"]

        # right of 6 is right of 3 approaching leftwards, use inverse q6_y as q3_y
        if q0 == 6:
            l_x, l_y = global_to_local_coords(x, y)
            if grid[149 - l_y][99] == ".":
                pos = [99, 149 - l_y, "<"]

    elif facing == "<":
        # left of 1 is top of 5 approching downwards, use q1_y as q5_x
        if q0 == 1:
            l_x, l_y = local_to_global_coords(l_y, 0, 5)
            if grid[0][l_x] == ".":
                pos = [l_x, 0, "v"]

        # left of 2 is left of 5 approaching rightwards, use inverse q2_y as q5_y
        if q0 == 2:
            l_x, l_y = global_to_local_coords(x, y)
            if grid[49 - l_y][50] == ".":
                pos = [50, 49 - l_y, ">"]

        # left of 4 is top of 2 approaching downwards, use q4_y as q2_x
        if q0 == 4:
            l_x, l_y = local_to_global_coords(l_y, 0, 2)
            if grid[100][l_x] == ".":
                pos = [l_x, 100, "v"]

        # left of 5 is left of 2 approaching rightwards, use inverse q5_y as q2_y
        if q0 == 5:
            l_x, l_y = global_to_local_coords(x, y)
            if grid[149 - l_y][0] == ".":
                pos = [0, 149 - l_y, ">"]

    elif facing == "v":
        # bottom of 1 is top of 6 approaching downwards, use q1_x as q6_x
        if q0 == 1:
            l_x, l_y = local_to_global_coords(l_x, 0, 6)
            if grid[0][l_x] == ".":
                pos = [l_x, 0, "v"]

        # bottom of 3 is right of 1 approaching leftwards, use q3_x as q1_y
        if q0 == 3:
            l_x, l_y = local_to_global_coords(0, l_x, 1)
            if grid[l_y][49] == ".":
                pos = [49, l_y, "<"]

        # bottom of 6 is right of 4 approaching leftwards, use q6_x as q4_y
        if q0 == 6:
            l_x, l_y = local_to_global_coords(0, l_x, 4)
            if grid[l_y][99] == ".":
                pos = [99, l_y, "<"]

    elif facing == "^":
        # top of 2 is left of 4 approaching leftwards, use q2_x as q4_y
        if q0 == 2:
            l_x, l_y = local_to_global_coords(0, l_x, 4)
            if grid[l_y][50] == ".":
                pos = [50, l_y, ">"]

        # top of 5 is left of 1 approaching rightwards, use q5_x as q1_y
        if q0 == 5:
            lx_, l_y = local_to_global_coords(0, l_x, 1)
            if grid[l_y][0] == ".":
                pos = [0, l_y, ">"]

        # top of 6 is bottom of 1 approaching upwards, use q6_x as q1_x
        if q0 == 6:
            lx_, l_y = local_to_global_coords(l_x, 0, 1)
            if grid[199][l_x] == ".":
                pos = [l_x, 199, "^"]

    return pos


def process_direction(
    grid: list[list[str]], pos: list[str | int], dir: tuple[int, str]
) -> tuple[list[list[str]], list[str | int]]:
    global display_grid, f, c
    steps, turn = dir

    for _ in range(steps):
        x, y, facing = pos
        x = int(x)
        y = int(y)

        display_grid[y][x] = facing

        q = get_quadrant(x, y)

        if facing == ">":
            # if next step wraps around
            if x == (len(grid[y]) - 1) or grid[y][x + 1] == " ":
                pos = step_boundary(grid, pos)
            elif grid[y][x + 1] == ".":
                pos[0] = int(pos[0]) + 1
            elif grid[y][x + 1] == "#":
                break
        if facing == "<":
            # if next step wraps around
            if x == 0 or grid[y][x - 1] == " ":
                pos = step_boundary(grid, pos)
            elif grid[y][x - 1] == ".":
                pos[0] = int(pos[0]) - 1
            elif grid[y][x - 1] == "#":
                break

        if facing == "^":
            # if next step wraps around
            if y == 0 or grid[y - 1][x] == " ":
                pos = step_boundary(grid, pos)
            elif grid[y - 1][x] == ".":
                pos[1] = int(pos[1]) - 1
            elif grid[y - 1][x] == "#":
                break

        if facing == "v":
            # if next step wraps around
            if y == (len(grid) - 1) or grid[y + 1][x] == " ":
                pos = step_boundary(grid, pos)
            elif grid[y + 1][x] == ".":
                pos[1] = int(pos[1]) + 1
            elif grid[y + 1][x] == "#":
                break

    if turn in ["L", "R"]:
        pos[2] = turn_dict[str(pos[2])][turn]

    return grid, pos


def get_score(lines: list[str]) -> int:
    global display_grid
    score = 0
    is_map = True
    max_len = 0
    start_x = 0
    directions: list[tuple[int, str]] = []

    grid: list[list[str]] = []

    for line in lines:
        if line == "\n":
            is_map = False
            continue

        if is_map:
            grid.append([c for c in line.replace("\n", "")])
            if len(grid[-1]) > max_len:
                max_len = len(grid[-1])
        if not is_map:
            d_str = line.strip() + "."
            directions = [
                (int(steps), direction)
                for steps, direction in re.findall(r"(\d+)([LR\.])", d_str)
            ]

    display_grid = copy.deepcopy(grid)

    start_x = fill_grid(grid, max_len)
    pos = [start_x, 0, ">"]

    for dir in directions:
        grid, pos = process_direction(grid, pos, dir)

    pos[0] = int(pos[0]) + 1
    pos[1] = int(pos[1]) + 1
    score = (
        (int(pos[1])) * 1000
        + (int(pos[0])) * 4
        + [">", "v", "<", "^"].index(str(pos[2]))
    )

    return score


# end_get_score


if __name__ == "__main__":
    lines = get_lines("input.txt")
    score = get_score(lines)

    print(f"Score: {score}")
