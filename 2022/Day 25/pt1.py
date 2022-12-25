def get_lines(filename: str):
    lines = []

    f = open(filename, "r")
    for line in f:
        lines.append(line)

    f.close()
    return lines
# end_get_lines


def to_int(line: str) -> int:
    s = 0
    i = 1
    for c in line.strip()[::-1]:
        if c.isdigit():
            s += i * int(c)
        elif c == '-':
            s -= i
        elif c == '=':
            s -= (2*i)
        i *= 5
    return s


def to_snafu(num) -> str:
    if num != 0:
        n = num % 5
        if n in [0, 1, 2]:
            return to_snafu((num-n)//5) + str(n)
        elif n == 3:
            return to_snafu((num+2)//5) + '='
        elif n == 4:
            return to_snafu((num+1)//5) + '-'
    return ""


def get_score(lines: list[str]) -> str:
    sum = 0
    for line in lines:
        sum += to_int(line)
    x = to_snafu(sum)
    return x
# end_get_score


if __name__ == "__main__":
    lines = get_lines("input.txt")
    score = get_score(lines)

    print(f"Score: {score}")
