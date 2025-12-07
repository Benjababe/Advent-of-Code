import functools
import time

grid: list[list[str]] = []


def format_time(sec: float) -> str:
    if sec < 0.001:
        return f"{sec * 1_000_000:.2f} microseconds"
    elif sec < 1:
        return f"{sec * 1000:.2f} milliseconds"
    else:
        return f"{sec:.2f} seconds"


def get_lines(filename: str):
    lines = []

    f = open(filename, "r")
    for line in f:
        lines.append(line.strip())

    f.close()
    return lines


def get_score(lines: list[str], pt2: bool) -> int:
    global grid
    grid = [[c for c in line] for line in lines]
    score = 0

    if not pt2:
        for y, row in enumerate(grid[:-1]):
            for x, char in enumerate(row):
                if char not in ["S", "|"]:
                    continue

                if grid[y + 1][x] == "^":
                    if x > 0:
                        grid[y + 1][x - 1] = "|"
                    if x < (len(grid[0]) - 1):
                        grid[y + 1][x + 1] = "|"
                    score += 1
                else:
                    grid[y + 1][x] = "|"

    else:
        first_split = get_first_split(grid)
        score += spl(first_split[0], first_split[1]) + 1

    return score


def get_first_split(grid: list[list[str]]) -> tuple[int, int]:
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char == "^":
                for ny in range(y, -1, -1):
                    if grid[ny][x] == "S":
                        return (x, y)
    return (0, 0)


@functools.cache
def spl(x: int, y: int) -> int:
    global grid
    score = 1

    lx, rx = x - 1, x + 1
    l_done, r_done = False, False
    for ny in range(y + 1, len(grid)):
        if grid[ny][lx] == "^" and not l_done:
            score += spl(lx, ny)
            l_done = True
        if grid[ny][rx] == "^" and not r_done:
            score += spl(rx, ny)
            r_done = True

    return score


if __name__ == "__main__":
    lines = get_lines("input.txt")

    t1 = time.perf_counter()
    score_pt1 = get_score(lines, False)
    t2 = time.perf_counter()
    print(f"Score Pt1: {score_pt1}\tTime taken: {format_time(t2-t1)}")

    t1 = time.perf_counter()
    score_pt2 = get_score(lines, True)
    t2 = time.perf_counter()
    print(f"Score Pt2: {score_pt2}\tTime taken: {format_time(t2-t1)}")
