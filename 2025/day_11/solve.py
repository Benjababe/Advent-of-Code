import time
import functools

graph: dict[str, list[str]] = {}


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
    global graph

    for line in lines:
        device, output_str = line.split(": ")
        graph[device] = output_str.split()

    node = "svr" if pt2 else "you"
    score = traverse(node, False, False, pt2)
    return score


@functools.cache
def traverse(node: str, dac: bool, fft: bool, pt2: bool) -> int:
    global graph
    if node == "out":
        return 1 if (dac and fft) or not pt2 else 0

    dac |= node == "dac"
    fft |= node == "fft"
    return sum([traverse(out, dac, fft, pt2) for out in graph[node]])


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
