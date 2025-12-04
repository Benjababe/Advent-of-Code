
neighbours = [
    (-1,  0),
    (1,  0),
    (0, -1),
    (0,  1),
    (-1, -1),
    (-1,  1),
    (1, -1),
    (1,  1),
]


def get_lines(filename: str):
    lines = []

    f = open(filename, "r")
    for line in f:
        lines.append(line.strip())

    f.close()
    return lines


def get_score(lines: list[str], recurse: bool) -> int:
    grid = [[c for c in l] for l in lines]
    score = process_grid(grid, recurse)
    return score


def process_grid(grid: list[list[str]], recurse: bool) -> int:
    score = 0
    copy_grid = [[c for c in l] for l in grid]
    to_remove: list[tuple[int, int]] = []

    for y in range(len(grid)):
        line = grid[y]
        for x in range(len(line)):
            if grid[y][x] != "@":
                continue

            count = 0
            for dx, dy in neighbours:
                nx, ny = x+dx, y+dy
                if nx >= 0 and nx < len(grid[0]) and ny >= 0 and ny < len(grid):
                    if grid[ny][nx] == "@":
                        count += 1

            if count < 4:
                score += 1
                to_remove.append((x, y))
                copy_grid[y][x] = "X"

    if recurse and score > 0:
        for x, y in to_remove:
            grid[y][x] = "."
        score += process_grid(grid, recurse)

    return score


if __name__ == "__main__":
    lines = get_lines("input.txt")

    score_pt1 = get_score(lines, False)
    print(f"Pt1 Score: {score_pt1}")
    score_pt2 = get_score(lines, True)
    print(f"Pt2 Score: {score_pt2}")
