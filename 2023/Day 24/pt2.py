import subprocess

import z3


def get_lines(filename: str):
    lines = []

    f = open(filename, "r")
    for line in f:
        lines.append(line)

    f.close()
    return lines


def z3_cheating(stones: list[tuple[list[int], list[int]]]):
    x, y, z = z3.Real("x"), z3.Real("y"), z3.Real("z")
    dx, dy, dz = z3.Real("dx"), z3.Real("dy"), z3.Real("dz")
    s = z3.Solver()

    for i, ((sx, sy, sz), (sdx, sdy, sdz)) in enumerate(stones):
        t = z3.Real(f"t{i}")
        s.add(sx + sdx * t == x + dx * t)
        s.add(sy + sdy * t == y + dy * t)
        s.add(sz + sdz * t == z + dz * t)

    s.check()
    m = s.model()
    return eval(f"{m[x]} + {m[y]} + {m[z]}")


def get_init_pos(lines: list[str]) -> int:
    stones = []

    for line in lines:
        s1, s2 = line.strip().split("@")
        s1 = [int(pos) for pos in s1.strip().split(",")]
        s2 = [int(vel) for vel in s2.strip().split(",")]

        stones.append((s1, s2))

    pos_sum = z3_cheating(stones)
    return pos_sum


if __name__ == "__main__":
    lines = get_lines("input.txt")
    score = get_init_pos(lines)

    print(f"Sum of positions: {score}")
