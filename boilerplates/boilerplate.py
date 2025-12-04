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


def get_score(lines: list[str]) -> int:
    score = 0

    for line in lines:
        x = 0

    return score


if __name__ == "__main__":
    lines = get_lines("input.txt")

    t1 = time.perf_counter()
    score = get_score(lines)
    t2 = time.perf_counter()
    print(f"Score: {score}")
    print(f"Time taken: {format_time(t2-t1)}")

    if platform.system() == "Windows":
        subprocess.run("clip", text=True, input=str(score))
    elif platform.system() == "Darwin":
        subprocess.run("pbcopy", text=True, input=str(score))
    elif platform.system() == "Linux":
        subprocess.run(
            "xclip -selection clipboard", text=True, input=str(score), shell=True
        )

    print(f"{score} copied to the clipboard")
