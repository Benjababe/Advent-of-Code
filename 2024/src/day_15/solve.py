def get_lines(filename: str):
    lines = []

    f = open(filename, "r")
    for line in f:
        lines.append(line)

    f.close()
    return lines


def push(grid: list[list[str]], x: int, y: int, dx: int, dy: int, act: bool):
    if grid[y][x] == "#":
        return False
    if grid[y][x] == "." or grid[y][x] == " ":
        return True

    # if robot or moving box l->r, try to push by 1 space
    if dx != 0 or grid[y][x] == "@" or grid[y][x] == "O":
        p = push(grid, x + dx, y + dy, dx, dy, act)
        if grid[y + dy][x + dx] == ".":
            if act:
                grid[y + dy][x + dx] = grid[y][x]
                grid[y][x] = "."
            return True
        return p

    # if left box and moving vertically, push up/down and the space to the right
    elif grid[y][x] == "[":
        p = push(grid, x + dx, y + dy, dx, dy, act)
        q = push(grid, x + dx + 1, y + dy, dx, dy, act)

        # if wide box can be pushed, push it on actual run
        if grid[y + dy][x + dx] == "." and grid[y + dy][x + dx + 1] == ".":
            if act:
                grid[y + dy][x + dx] = "["
                grid[y + dy][x + dx + 1] = "]"
                grid[y][x] = "."
                grid[y][x + 1] = "."
            return True
        return p and q

    # if right box and moving vertically, push up/down and space to the left
    elif grid[y][x] == "]":
        p = push(grid, x + dx - 1, y + dy, dx, dy, act)
        q = push(grid, x + dx, y + dy, dx, dy, act)

        # if wide box can be pushed, push it on actual run
        if grid[y + dy][x + dx - 1] == "." and grid[y + dy][x + dx] == ".":
            if act:
                grid[y + dy][x + dx - 1] = "["
                grid[y + dy][x + dx] = "]"
                grid[y][x - 1] = "."
                grid[y][x] = "."
            return True
        return p and q

    return False


def get_score(lines: list[str], p2: bool) -> int:
    score = 0
    l = "".join(lines)

    if p2:
        l = (
            l.replace("#", "##")
            .replace("O", "[]")
            .replace(".", "..")
            .replace("@", "@.")
        )

    segments = l.split("\n\n")
    grid = [[c for c in l.strip()] for l in segments[0].split("\n")]

    x, y = 1, 1
    for ty in range(len(grid)):
        for tx in range(len(grid[ty])):
            if grid[ty][tx] == "@":
                x, y = tx, ty

    inst = segments[1].replace("\n", "")
    move_map = {"<": (-1, 0), ">": (1, 0), "^": (0, -1), "v": (0, 1)}
    for direc in inst:
        dx, dy = move_map[direc]
        p = push(grid, x, y, dx, dy, False)
        if p:
            push(grid, x, y, dx, dy, p)
            x += dx
            y += dy

    for ty in range(len(grid)):
        for tx in range(len(grid[ty])):
            if grid[ty][tx] == "[" or grid[ty][tx] == "O":
                score += tx + (ty * 100)

    return score


if __name__ == "__main__":
    lines = get_lines("input.txt")

    score = get_score(lines, False)
    print(f"Day 15 Part 1: {score}")

    score = get_score(lines, True)
    print(f"Day 15 Part 2: {score}")
