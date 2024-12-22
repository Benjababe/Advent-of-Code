import platform
import subprocess
from enum import Enum


class InputType(Enum):
    KEYPAD = 1
    DIRPAD = 2


diffs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

diff_map = {
    (-1, 0): "<",
    (1, 0): ">",
    (0, -1): "^",
    (0, 1): "v",
}


def get_lines(filename: str):
    lines = []

    f = open(filename, "r")
    for line in f:
        lines.append(line.strip())

    f.close()
    return lines


def in_pad(pad: list[list[str]], x: int, y: int) -> bool:
    return x >= 0 and x < len(pad[0]) and y >= 0 and y < len(pad) and pad[y][x] != " "


def get_inputs(code: str):
    keypad = [
        ["7", "8", "9"],
        ["4", "5", "6"],
        ["1", "2", "3"],
        [" ", "0", "A"],
    ]

    dirpad = [
        [" ", "^", "A"],
        ["<", "v", ">"],
    ]

    queue = [(2, 3, InputType.KEYPAD, [c for c in code], [], 0, set())]

    shortest = [2**32, 2**32, 2**32]

    while len(queue) > 0:
        x, y, inp_type, targets, path, dirpad_robots, visited = queue[0]
        del queue[0]
        pad = dirpad if inp_type == InputType.DIRPAD else keypad
        if (x, y) in visited:
            continue
        visited.add((x, y))

        s_i = 0
        if inp_type == InputType.DIRPAD:
            s_i = s_i + 1 + dirpad_robots

        if len(path) > shortest[s_i]:
            continue

        if len(targets) == 0:
            continue

        if inp_type == InputType.KEYPAD:
            if pad[y][x] == targets[0]:
                path.append("A")

                if len(targets) == 1:
                    # queue.clear()
                    queue.append((2, 0, InputType.DIRPAD, path.copy(), [], 0, set()))

                    if len(path) <= shortest[s_i]:
                        print("".join(path))
                        shortest[s_i] = len(path)
                else:
                    # queue.clear()
                    del targets[0]
                    queue.append(
                        (x, y, inp_type, targets.copy(), path.copy(), 0, set())
                    )

                continue

        elif inp_type == InputType.DIRPAD:
            if pad[y][x] == targets[0]:
                path.append("A")

                if len(targets) == 1:
                    if len(path) <= shortest[s_i]:
                        print("".join(path))
                        shortest[s_i] = len(path)
                    if dirpad_robots == 1:
                        print(len(path))

                    # queue.clear()
                    queue.append((2, 1, InputType.DIRPAD, path.copy(), [], 1, set()))
                    dirpad_robots += 1
                else:
                    # queue.clear()
                    del targets[0]
                    queue.append(
                        (
                            x,
                            y,
                            inp_type,
                            targets.copy(),
                            path.copy(),
                            dirpad_robots,
                            set(),
                        )
                    )

                continue

        if len(path) >= shortest[s_i]:
            continue

        for dx, dy in diffs:
            nx, ny = x + dx, y + dy
            if not in_pad(pad, nx, ny):
                continue
            np = path.copy()
            np.append(diff_map[(dx, dy)])
            queue.append(
                (nx, ny, inp_type, targets.copy(), np, dirpad_robots, visited.copy())
            )


def get_score(lines: list[str]) -> int:
    score = 0

    for code in lines:
        i = get_inputs(code.strip())
        print(i)

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
