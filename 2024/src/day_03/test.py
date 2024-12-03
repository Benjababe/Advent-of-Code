import subprocess
import re


def get_lines(filename: str):
    lines = []

    f = open(filename, "r")
    for line in f:
        lines.append(line)

    f.close()
    return lines


def find_all_indexes(text: str, substring: str) -> list[int]:
    indexes = []
    start = 0

    while start < len(text):
        index = text.find(substring, start)
        if index == -1:
            break
        indexes.append(index)
        start = index + 1

    return indexes


def get_score(lines: list[str]) -> int:
    sc1, sc2 = 0, 0

    pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
    do = True

    for line in lines:
        matches = re.findall(pattern, line.strip())

        for match in matches:
            sc1 += int(match[0]) * int(match[1])

        do_indexes = find_all_indexes(line, "do()")
        dont_indexes = find_all_indexes(line, "don't()")
        mul_indexes = [match.start() for match in re.finditer(pattern, line)]

        cur = 0

        for j, i in enumerate(mul_indexes):
            cur = i
            while len(do_indexes) > 0 and do_indexes[0] < i:
                if do_indexes[0] < cur:
                    do = True
                    cur = do_indexes[0]
                del do_indexes[0]

            while len(dont_indexes) > 0 and dont_indexes[0] < i:
                if dont_indexes[0] < cur:
                    do = False
                    cur = dont_indexes[0]
                del dont_indexes[0]

            if do:
                sc2 += int(matches[j][0]) * int(matches[j][1])

            pass

    return sc2


if __name__ == "__main__":
    lines = get_lines("input.txt")
    score = get_score(lines)

    print(f"Score: {score}")
    subprocess.run("clip", text=True, input=str(score))
    print(f"{score} copied to the clipboard")
