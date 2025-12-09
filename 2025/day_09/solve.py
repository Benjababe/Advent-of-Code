import platform
import subprocess
import time

Line = tuple[tuple[int, int], tuple[int, int]]


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
    r = [[int(c) for c in line.split(",")] for line in lines]
    rects = [(v[0], v[1]) for v in r]

    polygon = [(rects[i], rects[i+1]) for i in range(len(rects)-1)]
    polygon.append((rects[-1], rects[0]))

    largest = 0
    for i, (x0, y0) in enumerate(rects[:-1]):
        for (x1, y1) in rects[i+1:]:
            if pt2 and not line_contained_in_poly(((x0, y0), (x1, y1)), polygon):
                continue

            area = (abs(x1-x0)+1) * (abs(y1-y0)+1)
            if area > largest:
                largest = area
    score = largest

    return score


# Thank you reddit
def line_contained_in_poly(line: Line, polygon: list[Line]):
    p0, p1 = line
    x0, x1 = min(p0[0], p1[0]), max(p0[0], p1[0])
    y0, y1 = min(p0[1], p1[1]), max(p0[1], p1[1])

    for poly_line in polygon:
        pp0, pp1 = poly_line
        px0, px1 = min(pp0[0], pp1[0]), max(pp0[0], pp1[0])
        py0, py1 = min(pp0[1], pp1[1]), max(pp0[1], pp1[1])

        if x0 < px1 and x1 > px0 and y0 < py1 and y1 > py0:
            return False

    return True


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

    # Remove if unnecessary
    if platform.system() == "Windows":
        subprocess.run("clip", text=True, input=str(score_pt1))
    elif platform.system() == "Darwin":
        subprocess.run("pbcopy", text=True, input=str(score_pt1))
    elif platform.system() == "Linux":
        subprocess.run(
            "xclip -selection clipboard", text=True, input=str(score_pt1), shell=True
        )
    print(f"{score_pt1} copied to the clipboard")
