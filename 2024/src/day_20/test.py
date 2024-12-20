import platform
import subprocess
from collections import defaultdict

diffs = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def get_lines(filename: str):
    lines = []

    f = open(filename, "r")
    for line in f:
        lines.append(line.strip())

    f.close()
    return lines


def in_grid(grid: list[list[str]], x: int, y: int) -> bool:
    return x >= 0 and x < len(grid[0]) and y >= 0 and y < len(grid)


def base_traverse(grid: list[list[str]], x: int, y: int) -> tuple[int, list[tuple[int, int]], dict]:
    visited = set()
    queue = [(x, y, 0, [(x, y)])]
    step_map = {}

    while len(queue) > 0:
        x, y, steps, path = queue[0]
        del queue[0]
        if not in_grid(grid, x, y) or (x, y) in visited or grid[y][x] == '#':
            continue

        if grid[y][x] == 'E':
            step_map[(x, y)] = len(path)
            return steps, path, step_map

        step_map[(x, y)] = len(path)
        visited.add((x, y))

        for dx, dy in diffs:
            nx, ny = x+dx, y+dy
            p = path.copy()
            p.append((nx, ny))
            queue.append((nx, ny, steps+1, p))

    return 2**32, [], {}


def traverse(grid: list[list[str]], sx: int, sy: int, ex: int, ey: int, cheat_count: int) -> int:
    sc = 0
    base_steps, path, step_map = base_traverse(grid, sx, sy)
    empty_spots = []
    test = defaultdict(lambda: 0)

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] != '#':
                empty_spots.append((x, y))

    for dist_to_p, (px, py) in enumerate(path):
        for x, y in empty_spots:
            if x == px and y == py:
                continue

            cheat_dist = abs(x-px) + abs(y-py)
            if cheat_dist >= (cheat_count+1):
                continue

            rem_dist = base_steps - step_map[(x, y)] + 1
            total_dist = dist_to_p + cheat_dist + rem_dist

            if total_dist < base_steps:
                saved = base_steps - total_dist
                if saved >= 100:
                    sc += 1

    return sc


def get_score(lines: list[str]) -> int:
    score = 0
    grid = [[c for c in l] for l in lines]
    sx, sy, ex, ey = 0, 0, 0, 0

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == 'S':
                sx, sy = x, y
            if grid[y][x] == 'E':
                ex, ey = x, y

    score = traverse(grid, sx, sy, ex, ey, 20)
    return score


if __name__ == "__main__":
    lines = get_lines("input.txt")
    score = get_score(lines)

    print(f"Score: {score}")

    if platform.system() == "Windows":
        subprocess.run("clip", text=True, input=str(score))
    elif platform.system() == "Darwin":
        subprocess.run("pbcopy", text=True, input=str(score))
    elif platform.system() == "Linux":
        subprocess.run(
            "xclip -selection clipboard", text=True, input=str(score), shell=True
        )

    print(f"{score} copied to the clipboard")
