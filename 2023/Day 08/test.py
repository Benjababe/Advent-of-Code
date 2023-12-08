import subprocess
import math


def get_lines(filename: str):
    lines = []

    f = open(filename, "r")
    for line in f:
        lines.append(line)

    f.close()
    return lines

def all_z(arr):
    for a in arr:
        if not a.endswith("Z"):
            return False
    return True

def all_found(sh):
    for s in sh:
        if s == 0:
            return False
    return True



def get_score(lines: list[str]) -> int:
    score = 0
    inst = lines[0].strip()

    n = []
    nodes = {}

    for line in lines[2:]:
        orig = line.split("=")[0].strip()
        l, r = line.split("=")[1].replace("(", "").replace(")", "").split(", ")
        nodes[orig] = {"L": l.strip(), "R": r.strip()}

        if orig.endswith("A"):
            n.append(orig)

    shortest = [0 for no in n]

    while not all_z(n):
        for dir in inst:
            for i, cur_n in enumerate(n):
                n[i] = nodes[cur_n][dir]
                if n[i].endswith("Z") and shortest[i] == 0:
                    shortest[i] = score + 1
            if all_found(shortest):
                print(shortest, len(inst))
                lcm_shortest = math.lcm(*shortest, len(inst))
                x=0
                
            score += 1

    return score


if __name__ == "__main__":
    lines = get_lines("input.txt")
    score = get_score(lines)

    print(f"Score: {score}")
    # subprocess.run("clip", text=True, input=str(score))
    # print(f"{score} copied to the clipboard")
