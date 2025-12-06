import math
import time


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
        line = line.strip("\n")
        line += " "
        lines.append(line)

    f.close()
    return lines


def get_score(lines: list[str], pt2: bool) -> int:
    score = 0

    prev_blank = -1
    for x in range(len(lines[0])):
        if not is_col_blank(lines, x):
            continue

        tmp_n = [0] * ((x - prev_blank - 1) if pt2 else (len(lines) - 1))
        if pt2:
            for nx in range(x - 1, prev_blank, -1):
                for y in range(len(lines) - 1):
                    if lines[y][nx] == " ":
                        continue
                    idx = nx - prev_blank - 1
                    tmp_n[idx] = 10 * tmp_n[idx] + int(lines[y][nx])
        else:
            for y in range(len(lines) - 1):
                for nx in range(prev_blank, x):
                    if lines[y][nx] == " ":
                        continue
                    tmp_n[y] = 10 * tmp_n[y] + int(lines[y][nx])

        op = lines[-1][prev_blank + 1]
        if op == "+":
            score += sum(tmp_n)
        if op == "*":
            score += math.prod(tmp_n)

        prev_blank = x

    return score


def is_col_blank(lines: list[str], x: int) -> bool:
    for y in range(len(lines)):
        if lines[y][x] != " ":
            return False
    return True


if __name__ == "__main__":
    lines = get_lines("bigboy.txt")

    t1 = time.perf_counter()
    score_pt1 = get_score(lines, False)
    t2 = time.perf_counter()
    print(f"Score Pt1: {score_pt1}\tTime taken: {format_time(t2-t1)}")

    t1 = time.perf_counter()
    score_pt2 = get_score(lines, True)
    t2 = time.perf_counter()
    print(f"Score Pt2: {score_pt2}\tTime taken: {format_time(t2-t1)}")
