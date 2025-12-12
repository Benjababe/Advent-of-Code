import time
from copy import deepcopy

present_combos: list[list[list[list[str]]]] = []


class Region:
    def __init__(self, width: int, height: int, req: list[int]):
        self.width = width
        self.height = height
        self.req = req.copy()
        self.grid = [['.' for _ in range(width)] for _ in range(height)]


def format_time(sec: float) -> str:
    if sec < 0.001:
        return f"{sec * 1_000_000:.2f} microseconds"
    elif sec < 1:
        return f"{sec * 1000:.2f} milliseconds"
    else:
        return f"{sec:.2f} seconds"


def get_presents(filename: str):
    presents = []

    f = open(filename, "r")
    for present in f.read().split("\n\n"):
        presents.append(present.strip())

    f.close()
    return presents


def get_score(raw_presents: list[str]) -> int:
    score = 0

    presents = [[[c for c in row] for row in p.split()[1:]] for p in raw_presents[:-1]]
    present_usages = [sum([sum([1 if c == "#" else 0 for c in row]) for row in present]) for present in presents]

    raw_regions = raw_presents[-1].split("\n")
    for raw_region in raw_regions:
        raw_region_spl = raw_region.split()
        shape, req = raw_region_spl[0][:-1], [int(v) for v in raw_region_spl[1:]]
        dims = [int(d) for d in shape.split("x")]

        # What the fuck
        area = dims[0] * dims[1]
        area_needed = sum([present_usages[i] * count for i, count in enumerate(req)])
        if area_needed <= area:
            score += 1

        # Brootbros...
        # score += bruteforce(deepcopy(presents), Region(dims[0], dims[1], req.copy()))

    return score


def bruteforce(presents: list[list[list[str]]], region: Region) -> int:
    global present_combos
    score = 0

    for present in presents:
        present_permutations = [present, flip_x(present), flip_y(present)]
        for i in range(3):
            present = rotate_90(present)
            present_permutations.append(present.copy())
            present_permutations.append(flip_x(present))
            present_permutations.append(flip_y(present))

        prune: set[str] = set()
        for i in range(len(present_permutations)-1, -1, -1):
            grid_str = grid_to_str(present_permutations[i])
            if grid_str not in prune:
                prune.add(grid_str)
            else:
                del present_permutations[i]
        present_combos.append(deepcopy(present_permutations))

    score += 1 if put_present(region.grid, region.req) else 0
    return score


def rotate_90(grid: list[list[str]]) -> list[list[str]]:
    return [list(reversed(row)) for row in zip(*grid)]


def flip_y(grid: list[list[str]]) -> list[list[str]]:
    return grid.copy()[::-1]


def flip_x(grid: list[list[str]]) -> list[list[str]]:
    return [row[::-1] for row in grid]


def grid_to_str(grid: list[list[str]]) -> str:
    return "".join(["".join(row) for row in grid])


def put_present(grid: list[list[str]], req: list[int]) -> bool:
    if all([r == 0 for r in req]):
        return True

    present_idx = -1
    presents: list[list[list[str]]] = []
    new_req: list[int] = []
    for i, num in enumerate(req):
        if num > 0:
            present_idx = i
            presents = present_combos[i]
            new_req = [r if idx != i else r-1 for idx, r in enumerate(req)]
            break

    for present in presents:
        present_width, present_height = len(present[0]), len(present)
        for y in range(len(grid) - present_height + 1):
            for x in range(len(grid[y]) - present_width + 1):
                if grid[y][x] != ".":
                    continue

                new_grid, check = check_present_fit(grid, present, present_idx, x, y)
                if not check:
                    continue

                if put_present(new_grid, new_req):
                    return True

    return False


def check_present_fit(grid: list[list[str]], present: list[list[str]], p_i: int, px: int, py: int) -> tuple[list[list[str]], bool]:
    fill_coords = []
    for y in range(len(present)):
        for x in range(len(present[y])):
            if present[y][x] == "#":
                if grid[py+y][px+x] == ".":
                    fill_coords.append((px+x, py+y))
                else:
                    return [], False

    chars = "ABCDEF"
    new_grid = [[chars[p_i] if (x, y) in fill_coords else c for x, c in enumerate(row)] for y, row in enumerate(grid)]
    return new_grid, True


if __name__ == "__main__":
    raw_presents = get_presents("input.txt")

    t1 = time.perf_counter()
    score_pt1 = get_score(raw_presents)
    t2 = time.perf_counter()
    print(f"Score Pt1: {score_pt1}\tTime taken: {format_time(t2-t1)}")
