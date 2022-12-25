def get_lines(filename: str):
    lines = []

    f = open(filename, "r")
    for line in f:
        lines.append(line)

    f.close()
    return lines
# end_get_lines


def get_score(lines: list[str]) -> int:
    score = 0

    for line in lines:
        x = 0

    return score
# end_get_score


if __name__ == "__main__":
    lines = get_lines("input.txt")
    score = get_score(lines)

    print(f"Score: {score}")
