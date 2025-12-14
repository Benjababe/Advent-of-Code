import time
from collections import defaultdict
from itertools import permutations

DIRECTIONS = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
]


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
    score = 0
    grid = [[c for c in line] for line in lines]
    start = get_start_pos(grid)
    sushi_pos = get_sushi_pos(grid)
    nodes = [s for s in sushi_pos]
    nodes.insert(0, start)

    if not pt2:
        dist_map = defaultdict(lambda: {})
        dist_perms = list(permutations(nodes, 2))
        for (sx, sy), (dsx, dsy) in dist_perms:
            dist_map[(sx, sy)][(dsx, dsy)] = 0
            queue = [(sx, sy, 0)]
            visited = set()
            while len(queue) > 0:
                new_path_perm, y, steps = queue.pop(0)
                if (new_path_perm, y) in visited:
                    continue
                visited.add((new_path_perm, y))

                if not (0 <= new_path_perm < len(grid[0]) and 0 <= y < len(grid)):
                    continue
                if grid[y][new_path_perm] not in ["E", "0", "S"]:
                    continue

                if (new_path_perm, y) == (dsx, dsy):
                    dist_map[(sx, sy)][(dsx, dsy)] = steps + 1
                    break

                for dx, dy in DIRECTIONS:
                    queue.append((new_path_perm + dx, y + dy, steps + 1))

        path_perms = list(permutations(sushi_pos))
        for i, perm in enumerate(path_perms):
            new_path_perm = (start,) + perm + (start,)
            path_perms[i] = new_path_perm

        shortest_path = (len(grid) * len(grid[0])) * (len(sushi_pos) + 2)
        for perm in path_perms:
            path_len = 0
            for i in range(len(perm[:-1])):
                path_len += dist_map[perm[i]][perm[i + 1]]
            if path_len < shortest_path:
                shortest_path = path_len
        return shortest_path

    return score


def get_start_pos(grid: list[list[str]]) -> tuple[int, int]:
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == "E":
                return (x, y)
    return (0, 0)


def get_sushi_pos(grid: list[list[str]]) -> list[tuple[int, int]]:
    pos: list[tuple[int, int]] = []
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == "S":
                pos.append((x, y))
    return pos


if __name__ == "__main__":
    lines = get_lines("input.txt")

    t1 = time.perf_counter()
    score_pt1 = get_score(lines, False)
    t2 = time.perf_counter()
    print(f"Score Pt1: {score_pt1}\tTime taken: {format_time(t2-t1)}")
