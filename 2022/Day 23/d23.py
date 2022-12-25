from collections import defaultdict
from copy import deepcopy


def def_list():
    return []


class Elf:
    id: int
    choices: list[str] = ["N", "S", "W", "E"]

    def cycle_decision(self):
        tmp = self.choices[0]
        self.choices = self.choices[1:]
        self.choices.append(tmp)


def get_lines(filename: str):
    lines = []

    f = open(filename, "r")
    for line in f:
        lines.append(line)

    f.close()
    return lines
# end_get_lines


def elf_decision(grid, x, y) -> str:
    if grid[y][x+1] == '.' and grid[y][x-1] == '.' and grid[y+1][x] == '.' and grid[y-1][x] == '.'\
            and grid[y-1][x+1] == '.' and grid[y-1][x-1] == '.' and grid[y+1][x+1] == '.' and grid[y+1][x-1] == '.':
        return ""

    for d in grid[y][x].choices:
        if d == "N" and grid[y-1][x] == '.' and grid[y-1][x-1] == '.' and grid[y-1][x+1] == '.':
            return "N"

        if d == "S" and grid[y+1][x] == '.' and grid[y+1][x-1] == '.' and grid[y+1][x+1] == '.':
            return "S"

        if d == "W" and grid[y][x-1] == '.' and grid[y-1][x-1] == '.' and grid[y+1][x-1] == '.':
            return "W"

        if d == "E" and grid[y][x+1] == '.' and grid[y-1][x+1] == '.' and grid[y+1][x+1] == '.':
            return "E"

    return ""


def simulate_elves(lines: list[str]) -> tuple[int, int]:
    grid = []
    grid_10 = []
    loop_count = 0

    # insert padding for grid
    lines.insert(0, "." * len(lines[1].strip()))
    lines.append("." * len(lines[1].strip()))

    for line in lines:
        line = f".{line.strip()}."
        grid.append([c if c == '.' else Elf() for c in f"{line.strip()}"])

    while True:
        loop_count += 1

        # key = coord
        # val = list of initial elf positions
        proposals = defaultdict(def_list)

        # get all elves decisions, 1st half of round
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if isinstance(grid[y][x], Elf):
                    decision = elf_decision(grid, x, y)
                    grid[y][x].cycle_decision()

                    if decision == "N":
                        proposals[(x, y-1)].append((x, y))
                    elif decision == "S":
                        proposals[(x, y+1)].append((x, y))
                    elif decision == "W":
                        proposals[(x-1, y)].append((x, y))
                    elif decision == "E":
                        proposals[(x+1, y)].append((x, y))

        # elves have stopped moving
        if len(proposals) == 0:
            break

        # act on all elves decisions, 2nd half of round
        for new_coord in proposals:
            if len(proposals[new_coord]) == 1:
                o_x, o_y = proposals[new_coord][0]
                n_x, n_y = new_coord
                grid[n_y][n_x] = grid[o_y][o_x]
                grid[o_y][o_x] = '.'

        # pad out grid
        if any(isinstance(c, Elf) for c in grid[0]):
            grid.insert(0, ['.' for _ in range(len(grid[0]))])
        if any(isinstance(c, Elf) for c in grid[-1]):
            grid.append(['.' for _ in range(len(grid[0]))])

        if any(isinstance(grid[y][0], Elf) for y in range(len(grid))):
            for y in range(len(grid)):
                grid[y].insert(0, '.')
        if any(isinstance(grid[y][-1], Elf) for y in range(len(grid))):
            for y in range(len(grid)):
                grid[y].append('.')

        if loop_count == 10:
            grid_10 = deepcopy(grid)

    x0, x1, y0, y1 = len(grid_10[0]), 0, len(grid_10), 0
    elf_count = 0

    # gets minimal size of the grid that will contain the elves
    for y in range(len(grid_10)):
        for x in range(len(grid_10[y])):
            if isinstance(grid_10[y][x], Elf):
                if x < x0:
                    x0 = x
                if x > x1:
                    x1 = x
                if y < y0:
                    y0 = y
                if y > y1:
                    y1 = y
                elf_count += 1

    board_size = (x1-x0+1) * (y1-y0+1)
    ground_tiles = board_size - elf_count

    return (ground_tiles, loop_count)
# end_get_score


if __name__ == "__main__":
    lines = get_lines("input.txt")
    tiles, loop_count = simulate_elves(lines)

    print(f"Empty ground tiles: {tiles}")
    print(f"Elves stop moving at loop: {loop_count}")
