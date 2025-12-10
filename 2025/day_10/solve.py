import time

import itertools
from collections import defaultdict

from pulp import LpProblem, LpVariable, LpInteger, value, PULP_CBC_CMD


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

    if not pt2:
        for line in lines:
            spl = line.split()
            target_lights = spl[0][1:-1]
            buttons = [[int(v) for v in btn[1:-1].split(",")] for btn in spl[1:-1]]

            queue = [("." * len(target_lights), 0)]
            visited = defaultdict(lambda: float('inf'))
            while len(queue) > 0:
                cur_lights, presses = queue.pop(0)

                # Skip already processed state
                if cur_lights in visited and visited[cur_lights] <= presses:
                    continue
                visited[cur_lights] = presses

                if cur_lights == target_lights:
                    score += presses
                    break

                for button in buttons:
                    new_lights = press_button_lights(cur_lights, button)
                    queue.append((new_lights, presses+1))

    else:
        for line in lines:
            spl = line.split()
            target_joltage = [int(c) for c in spl[-1][1:-1].split(",")]
            buttons = [[int(v) for v in btn[1:-1].split(",")] for btn in spl[1:-1]]

            lp_vars = []
            for i in range(len(buttons)):
                v = LpVariable(chr(ord('a') + i), lowBound=0, cat=LpInteger)
                lp_vars.append(v)

            prob = LpProblem("MinSumOfCoefficients")
            for i in range(len(target_joltage)):
                eq = 0
                for j, btn in enumerate(buttons):
                    if i not in btn:
                        continue
                    eq += lp_vars[j] * 1
                prob += eq == target_joltage[i]

            # Include this to specify to solve for minimum sum of coefficients (Very impt!!)
            eq = 0
            for lp_var in lp_vars:
                eq += lp_var
            prob += eq

            # By the powers of linear algebra I summon thee
            prob.solve(solver=PULP_CBC_CMD(msg=False))
            for i, lp_var in enumerate(lp_vars):
                score += int(value(lp_var))

    return score


def press_button_lights(cur_lights: str, button: list[int]) -> str:
    new_lights = [l for l in cur_lights]
    for i in button:
        new_lights[i] = "." if new_lights[i] == "#" else "#"
    return "".join(new_lights)


if __name__ == "__main__":
    lines = get_lines("input.txt")

    t1 = time.perf_counter()
    score_pt1 = get_score(lines, False)
    t2 = time.perf_counter()
    print(f"Score Pt1: {score_pt1}\tTime taken: {format_time(t2-t1)}")

    # t1 = time.perf_counter()
    # score_pt2 = get_score(lines, True)
    # t2 = time.perf_counter()
    # print(f"Score Pt2: {score_pt2}\tTime taken: {format_time(t2-t1)}")
