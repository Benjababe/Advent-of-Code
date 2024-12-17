import platform
import subprocess
import sys


def get_lines(filename: str):
    lines = []

    f = open(filename, "r")
    for line in f:
        lines.append(line.strip())

    f.close()
    return lines


def run_program(a: int, b: int, c: int, prog: list[str]) -> str:
    score = []

    i = 0
    while i < len(prog):
        p = prog[i]
        lit = int(prog[i+1])

        cmb = int(lit)
        if cmb == 4:
            cmb = a
        elif cmb == 5:
            cmb = b
        elif cmb == 6:
            cmb = c

        if p == '0':
            num = a
            denom = 2**cmb
            a = num // denom
        elif p == '1':
            b = b ^ lit
        elif p == '2':
            b = cmb % 8
        elif p == '3':
            if a != 0:
                i = lit*2 - 2
        elif p == '4':
            b = b ^ c
        elif p == '5':
            score.append(str(cmb % 8))
        elif p == '6':
            num = a
            denom = 2**cmb
            b = num // denom
        elif p == '7':
            num = a
            denom = 2**cmb
            c = num // denom

        i += 2

    return ",".join(score).strip()


def get_score(lines: list[str], p2: bool) -> str:
    prog = lines[-1].split(" ")[1].strip()
    prog_spl = prog.split(",")
    print(prog)

    a = int(lines[0].split(":")[1])
    b = int(lines[1].split(":")[1])
    c = int(lines[2].split(":")[1])

    if p2:
        mult = 0
        if len(sys.argv) > 1:
            mult = int(sys.argv[1])

        leng = 1000000000000000
        start = leng * mult
        stop = start + leng
        for a in range(start, stop):
            s = run_program(a, b, c, prog_spl)
            if s == prog:
                return str(a)

    else:
        out = run_program(a, b, c, prog_spl)
        return out

    return "-1"


if __name__ == "__main__":
    lines = get_lines("input.txt")
    score = get_score(lines, True)

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
