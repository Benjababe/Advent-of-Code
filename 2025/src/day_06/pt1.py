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
        line = line.replace("\n", "")
        line +=  " "
        lines.append(line)

    f.close()
    return lines


def get_score(lines: list[str], pt2: bool) -> int:
    score = 0
    nums: list[list[int]] = []

    if not pt2:
        for i, line in enumerate(lines):
            x = 0

            if i == len(lines)-1:
                ops = line.split()
                for j, op in enumerate(ops):
                    ns = nums[j]

                    val = ns[0]

                    for n in ns[1:]:
                        if op == "+":
                            val += n
                        elif op == "*":
                            val *= n

                    score += val

            else:
                line_nums = [int(n) for n in line.split()]
                for j in range(len(line_nums)):
                    if j >= len(nums):
                        nums.append([])
                    nums[j].append(line_nums[j])
    
    else:
        prev_blank = -1
        nums: list[list[int]] = []
        grid = [[c for c in line] for line in lines]
        for x in range(len(grid[0])):
            if not is_col_blank(grid, x):
                continue

            tmp_n = [0] * (x-prev_blank-1)
            op = ""
            for nx in range(x-1, prev_blank, -1):
                for y in range(len(grid)-1):
                    if grid[y][nx] == " ":
                        continue
                    
                    idx = nx-prev_blank-1
                    tmp_n[idx] = 10*tmp_n[idx] + int(grid[y][nx])
        
                if grid[-1][nx] == "+" or grid[-1][nx] == "*":
                    op = grid[-1][nx]

            v = 0
            if op == "+":
                v = sum(tmp_n)
            if op == "*":
                v = 1
                for px in tmp_n:
                    v *= px
            score += v
            prev_blank = x


    return score


def is_col_blank(grid: list[list[str]], x: int) -> bool:
    for y in range(len(grid)):
        if grid[y][x] != " ":
            return False
    return True


if __name__ == "__main__":
    lines = get_lines("input.txt")

    # t1 = time.perf_counter()
    # score_pt1 = get_score(lines, False)
    # t2 = time.perf_counter()
    # print(f"Score Pt1: {score_pt1}\tTime taken: {format_time(t2-t1)}")

    t1 = time.perf_counter()
    score_pt1 = get_score(lines, True)
    t2 = time.perf_counter()
    print(f"Score Pt2: {score_pt1}\tTime taken: {format_time(t2-t1)}")

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
