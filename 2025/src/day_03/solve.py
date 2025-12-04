
def get_lines(filename: str):
    lines = []

    f = open(filename, "r")
    for line in f:
        lines.append(line.strip())

    f.close()
    return lines


def get_score_pt1(lines: list[str]) -> int:
    score = 0
    for line in lines:
        score += process(line, 2)
    return score


def get_score_pt2(lines: list[str]) -> int:
    score = 0
    for line in lines:
        score += process(line, 12)
    return score


def process(line: str, battery_count: int) -> int:
    l, r = len(line) - battery_count, len(line)-1

    s = 0
    prev_l = -1
    for start_l in range(l, r+1):
        largest, largest_i = -1, -1
        for tmp_l in range(start_l, prev_l, -1):
            v = int(line[tmp_l])
            if v >= largest:
                largest = v
                largest_i = tmp_l

        s = s*10 + largest
        prev_l = largest_i

    return s


if __name__ == "__main__":
    lines = get_lines("input.txt")

    score_pt1 = get_score_pt1(lines)
    print(f"Pt1 Score: {score_pt1}")
    score_pt2 = get_score_pt2(lines)
    print(f"Pt2 Score: {score_pt2}")
