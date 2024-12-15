import re

import z3


def get_lines(filename: str):
    lines = []

    f = open(filename, "r")
    for line in f:
        lines.append(line)

    f.close()
    return lines


def get_tokens(ax: int, ay: int, bx: int, by: int, tx: int, ty: int, p2: bool) -> int:
    solver = z3.Solver()

    if p2:
        tx += 10000000000000
        ty += 10000000000000

    a, b = z3.Ints("a b")
    solver.add(
        ax * a + bx * b == (tx),
        ay * a + by * b == (ty),
    )

    if solver.check() == z3.sat:
        model = solver.model()
        a_val, b_val = model.eval(a), model.eval(b)
        if isinstance(a_val, z3.IntNumRef) and isinstance(b_val, z3.IntNumRef):
            return a_val.as_long() * 3 + b_val.as_long()

    return 0


def get_score(lines: list[str], p2: bool) -> int:
    score = 0

    l = "".join(lines)
    l = l.split("\n\n")

    a_re = re.compile(r"Button A: X\+(\d+), Y\+(\d+)")
    b_re = re.compile(r"Button B: X\+(\d+), Y\+(\d+)")
    t_re = re.compile(r"Prize: X=(\d+), Y=(\d+)")

    for seg in l:
        a_line, b_line, t_line = seg.split("\n")

        am = a_re.search(a_line)
        bm = b_re.search(b_line)
        tm = t_re.search(t_line)

        if am is not None:
            ax, ay = int(am.group(1)), int(am.group(2))
        if bm is not None:
            bx, by = int(bm.group(1)), int(bm.group(2))
        if tm is not None:
            tx, ty = int(tm.group(1)), int(tm.group(2))

        tokens = get_tokens(ax, ay, bx, by, tx, ty, p2)
        score += tokens

    return score


if __name__ == "__main__":
    lines = get_lines("input.txt")

    score = get_score(lines, False)
    print(f"Day 13 Part 1: {score}")

    score = get_score(lines, True)
    print(f"Day 13 Part 2: {score}")
