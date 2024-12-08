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


def process_direction(
    grid: list[list[str]], pos: list[str | int], dir: tuple[int, str]
) -> tuple[list[list[str]], list[str | int]]:
    global display_grid
    steps, turn = dir
    print(f"Currently at ({pos[0]}, {pos[1]}), facing {pos[2]}. Moving {steps} steps")

    for _ in range(steps):
        x, y, facing = pos
        x = int(x)
        y = int(y)

        display_grid[y][x] = facing

        if facing == ">":
            # if next step wraps around
            if x == (len(grid[y]) - 1) or grid[y][x + 1] == " ":
                for s in range(1, len(grid[y])):
                    t_x = x + s
                    if t_x >= len(grid[y]):  # wrap if it goes out of bounds
                        t_x -= len(grid[y])
                    if (
                        grid[y][t_x] == "#"
                    ):  # stop if walled before wrapping around properly
                        break
                    if grid[y][t_x] == ".":  # found a place to wrap around
                        pos[0] = t_x
                        break
            elif grid[y][x + 1] == ".":
                pos[0] = int(pos[0]) + 1
            elif grid[y][x + 1] == "#":
                break
        if facing == "<":
            # if next step wraps around
            if x == 0 or grid[y][x - 1] == " ":
                for s in range(1, len(grid[y])):
                    t_x = x - s
                    if t_x < 0:  # wrap if it goes out of bounds
                        t_x += len(grid[y])
                    if (
                        grid[y][t_x] == "#"
                    ):  # stop if walled before wrapping around properly
                        break
                    if grid[y][t_x] == ".":  # found a place to wrap around
                        pos[0] = t_x
                        break
            elif grid[y][x - 1] == ".":
                pos[0] = int(pos[0]) - 1
            elif grid[y][x - 1] == "#":
                break

        if facing == "^":
            # if next step wraps around
            if y == 0 or grid[y - 1][x] == " ":
                for s in range(1, len(grid)):
                    t_y = y - s
                    if t_y < 0:  # wrap if it goes out of bounds
                        t_y += len(grid)
                    if (
                        grid[t_y][x] == "#"
                    ):  # stop if walled before wrapping around properly
                        break
                    if grid[t_y][x] == ".":  # found a place to wrap around
                        pos[1] = t_y
                        break
            elif grid[y - 1][x] == ".":
                pos[1] = int(pos[1]) - 1
            elif grid[y - 1][x] == "#":
                break

        if facing == "v":
            # if next step wraps around
            if y == (len(grid) - 1) or grid[y + 1][x] == " ":
                for s in range(1, len(grid)):
                    t_y = y + s
                    if t_y >= len(grid):  # wrap if it goes out of bounds
                        t_y -= len(grid)
                    if (
                        grid[t_y][x] == "#"
                    ):  # stop if walled before wrapping around properly
                        break
                    if grid[t_y][x] == ".":  # found a place to wrap around
                        pos[1] = t_y
                        break
            elif grid[y + 1][x] == ".":
                pos[1] = int(pos[1]) + 1
            elif grid[y + 1][x] == "#":
                break

    print(f"Reached ({pos[0]},{pos[1]})")

    if turn in ["L", "R"]:
        print(f"Turning {turn} from {pos[2]} to {turn_dict[str(pos[2])][turn]}")
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

    for g in display_grid:
        print("".join(g))

    print(pos)

    return score


# end_get_score


if __name__ == "__main__":
    lines = get_lines("input.txt")
    score = get_score(lines)

    print(f"Score: {score}")
