
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


def get_score(lines: list[str], repeat: bool) -> int:
    grid = [[c for c in l] for l in lines]
    to_remove: list[tuple[int, int]] = []
    score = 0

    while True:
        iter_score = 0
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
                    iter_score += 1
                    to_remove.append((x, y))

        score += iter_score
        if repeat and iter_score > 0:
            for x, y in to_remove:
                grid[y][x] = "."
            continue
        break

    return score


if __name__ == "__main__":
    lines = get_lines("input.txt")

    score_pt1 = get_score(lines, False)
    print(f"Pt1 Score: {score_pt1}")
    score_pt2 = get_score(lines, True)
    print(f"Pt2 Score: {score_pt2}")
