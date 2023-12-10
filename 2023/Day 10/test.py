import subprocess
import sys

sys.setrecursionlimit(100000)

double_grid = []
test_grid = []
pt2_grid = []
max_dist = 0
visited = set()
visited2 = set()
s_val = ""
i_count = 0


def get_lines(filename: str):
    lines = []

    f = open(filename, "r")
    for line in f:
        lines.append(line)

    f.close()
    return lines


def dfs(lines, coords, steps):
    global max_dist, visited, test_grid

    x, y = coords
    cur_pipe = lines[y][x]
    possible = []

    if x == 3 and y == 3:
        pass

    if coords in visited and steps >= test_grid[y][x]:
        return steps

    if test_grid[y][x] == "." or steps < test_grid[y][x]:
        test_grid[y][x] = steps

    if steps > max_dist:
        max_dist = steps

    visited.add((x, y))

    if x > 0 and lines[y][x - 1] in ["F", "L", "-"]:
        if cur_pipe in ["S", "-", "J", "7"]:
            possible.append((x - 1, y))

    if x < (len(lines[0].strip()) - 1) and lines[y][x + 1] in ["J", "7", "-"]:
        if cur_pipe in ["S", "-", "F", "L"]:
            possible.append((x + 1, y))

    if y > 0 and lines[y - 1][x] in ["F", "7", "|"]:
        if cur_pipe in ["S", "|", "L", "J"]:
            possible.append((x, y - 1))

    if y < (len(lines) - 1) and lines[y + 1][x] in ["L", "J", "|"]:
        if cur_pipe in ["S", "|", "7", "F"]:
            possible.append((x, y + 1))

    for x, y in possible[::-1]:
        dfs(lines, (x, y), steps + 1)


def get_score(lines: list[str]) -> int:
    global test_grid, visited, pt2_grid, s_val
    score = 0
    test_grid = [["." for _ in line.strip()] for line in lines]
    pt2_grid = [[c for c in line.strip()] for line in lines]

    start = ""

    for y, line in enumerate(lines):
        for x, char in enumerate([char for char in line]):
            if char == "S":
                start = (x, y)

    dfs(lines, start, 0)

    m_len = 0
    for x, y in visited:
        dist = test_grid[y][x]
        if dist > score:
            score = dist

    pt2(lines)

    return score


def bfs(lines: list[str], x: int, y: int, free: bool = False) -> bool:
    global pt2_grid, visited, visited2, double_grid, i_count

    if (x, y) in visited2:
        return free

    visited2.add((x, y))

    x_max, y_max = len(double_grid[0]) - 1, len(double_grid) - 1

    if x == 0 or x == x_max or y == 0 or y == y_max:
        free = True

    diffs = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    for dx, dy in diffs:
        nx, ny = x + dx, y + dy

        if nx < 0 or nx > x_max or ny < 0 or ny > y_max:
            continue

        if double_grid[ny][nx] in [" ", "."]:
            res = bfs(double_grid, nx, ny, free)
            if res is True:
                free = res

    if double_grid[y][x] == ".":
        if not free:
            i_count += 1
        double_grid[y][x] = "O" if free else "I"

    return free


def pt2(lines: list[str]):
    global double_grid, i_count, visited
    double_grid = []
    for y, line in enumerate(lines):
        l1 = []
        l2 = []

        for x, char in enumerate(line.strip()):
            if (x, y) in visited:
                if char in ["-", "F", "L"]:
                    l1.extend(["*", "*"])
                elif char in ["|", "J", "7"]:
                    l1.extend(["*", " "])
                elif char == "S":
                    l1.extend(["*", "*"])
                else:
                    l1.extend(["*", "*"])

                if char in ["-", "L", "J"]:
                    l2.extend([" ", " "])
                elif char in ["|", "7", "F"]:
                    l2.extend(["*", " "])
                elif char == "S":
                    l2.extend(["*", "*"])
                else:
                    l2.extend([" ", " "])
            else:
                l1.extend([".", " "])
                l2.extend([" ", " "])

        double_grid.append(l1)
        double_grid.append(l2)

    with open("output.txt", "w") as f:
        s = "\n".join(["".join(line) for line in double_grid])
        f.write(s)
        f.close()

    for y, line in enumerate(double_grid):
        for x, char in enumerate([char for char in line]):
            if (x // 2, y // 2) not in visited:
                t = bfs(lines, x, y)
                pass

    print(f"Num of trapped cells: {i_count}")


if __name__ == "__main__":
    lines = get_lines("input.txt")
    score = get_score(lines)

    print(f"Score: {score}")
    subprocess.run("clip", text=True, input=str(score))
    print(f"{score} copied to the clipboard")
