import re


def get_lines(filename: str):
    lines = []

    f = open(filename, "r")
    for line in f:
        lines.append(line.strip())

    f.close()
    return lines


def get_score(lines: list[str], repeat_count: str) -> int:
    score = 0
    pattern = re.compile(rf"^(.+)\1{repeat_count}$")

    for line in lines:
        pairs = line.split(",")
        pairs = [[int(v) for v in pair.split("-")] for pair in pairs if len(pair) > 0]

        for l, r in pairs:
            for i in range(l, r+1):
                s = str(i)
                m = bool(pattern.match(s))
                if m:
                    score += int(s)

    return score


if __name__ == "__main__":
    lines = get_lines("input.txt")

    score_pt1 = get_score(lines, "{1}")
    print(f"Pt1 Score: {score_pt1}")
    score_pt2 = get_score(lines, "+")
    print(f"Pt2 Score: {score_pt2}")
