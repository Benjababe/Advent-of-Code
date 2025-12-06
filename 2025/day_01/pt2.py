import platform
import subprocess
import math


def get_lines(filename: str):
    lines = []

    f = open(filename, "r")
    for line in f:
        lines.append(line.strip())

    f.close()
    return lines


def get_score(lines: list[str]) -> int:
    score, pts = 0, 50

    for line in lines:
        d, val = line[0], int(line[1:])
        diff, mult = (100-pts), 1
        if d == "L":
            diff = pts
            mult = -1

        if pts == 0:
            diff = 100

        rem = val - diff
        if rem >= 0:
            score += 1
            score += rem // 100

        pts = (pts + mult*val) % 100

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
