import platform
import subprocess
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
        lines.append(line.strip())

    f.close()
    return lines


def get_score(lines: list[str], pt2: bool) -> int:
    score = 0
    sections = "\n".join(lines).split("\n\n")
    fresh_ranges, available_ids = sections
    fresh_range_tuples = [(int(r.split("-")[0]), int(r.split("-")[1])) for r in fresh_ranges.split("\n")]
    available_ids = [int(id) for id in available_ids.split("\n")]

    fresh_range_tuples.sort(key=lambda r: r[0])
    i = 0
    while i < len(fresh_range_tuples)-1:
        j = i+1
        while j < len(fresh_range_tuples) and fresh_range_tuples[j][0] <= fresh_range_tuples[i][1]:
            fresh_range_tuples[i] = (fresh_range_tuples[0][0], max(fresh_range_tuples[i][1], fresh_range_tuples[j][1]))
            del fresh_range_tuples[j]
        i += 1

    if pt2:
        for l, r in fresh_range_tuples:
            score += (r-l+1)
    else:
        for id in available_ids:
            is_fresh = False
            for l, r in fresh_range_tuples:
                if l <= id <= r:
                    is_fresh = True
            if is_fresh:
                score += 1

    return score


if __name__ == "__main__":
    lines = get_lines("input.txt")

    t1 = time.perf_counter()
    score_pt1 = get_score(lines, False)
    t2 = time.perf_counter()
    print(f"Score Pt1: {score_pt1}\tTime taken: {format_time(t2-t1)}")

    t1 = time.perf_counter()
    score_pt2 = get_score(lines, True)
    t2 = time.perf_counter()
    print(f"Score Pt2: {score_pt2}\tTime taken: {format_time(t2-t1)}")
