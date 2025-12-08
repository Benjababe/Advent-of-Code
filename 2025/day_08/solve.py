import platform
import subprocess
import time
import sys
import math


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
    boxes: list[tuple[int, int, int]] = []
    for line in lines:
        chars = line.split(",")
        boxes.append((int(chars[0]), int(chars[1]), int(chars[2])))

    boxes_with_dist: list[tuple[float, tuple[int, int, int], tuple[int, int, int]]] = []
    for i, box in enumerate(boxes):
        for j, nbox in enumerate(boxes):
            if i == j:
                continue
            dist = math.dist(box, nbox)
            boxes_with_dist.append((dist, min(box, nbox), max(box, nbox)))

    boxes_with_dist = list(set(boxes_with_dist))
    boxes_with_dist.sort(key=lambda b: b[0])

    conn_count = 0
    circuits: list[list[tuple[int, int, int]]] = [[box] for box in boxes]
    for i, (dist, box, nbox) in enumerate(boxes_with_dist):
        if conn_count == 1000 and not pt2:
            circuits.sort(key=lambda c: len(c), reverse=True)
            score = len(circuits[0]) * len(circuits[1]) * len(circuits[2])
            return score

        i1, i2 = find_circuit_index(circuits, box), find_circuit_index(circuits, nbox)
        if i1 != i2:
            circuits[i1].extend(circuits[i2])
            circuits[i2] = []
        circuits = [c for c in circuits if len(c) > 0]
        conn_count += 1

        if len(circuits) == 1 and pt2:
            score = box[0] * nbox[0]
            return score

    return score


def find_circuit_index(circuits: list[list[tuple[int, int, int]]], box: tuple[int, int, int]) -> int:
    for i in range(len(circuits)):
        if box in circuits[i]:
            return i
    return -1


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
