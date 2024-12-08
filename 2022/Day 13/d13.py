from functools import cmp_to_key


def get_lines(filename: str):
    lines = []

    f = open(filename, "r")
    for line in f:
        lines.append(line.strip())

    f.close()
    return lines


# end_get_lines


def check_packets(l: list, r: list):
    # pairs each value in lists, skips those without a pair
    for a, b in zip(l, r):
        # if both are integers, do basic check
        if type(a) == int and type(b) == int:
            if a < b:
                return True
            elif a > b:
                return False
            else:
                pass

        # if both are lists, recursive call to break it down further
        elif type(a) == list and type(b) == list:
            result = check_packets(a, b)
            if isinstance(result, bool):
                return result

        # if either is list, convert the integer to list and recursive call
        elif type(a) == int and type(b) == list:
            result = check_packets([a], b)
            if isinstance(result, bool):
                return result

        elif type(b) == int and type(a) == list:
            result = check_packets(a, [b])
            if isinstance(result, bool):
                return result

    # if lengths don't match, find way to break the tie if no correct order was confirmed found
    if len(l) > len(r):
        return False
    elif len(r) > len(l):
        return True
    else:
        return None


# end_check_packets


# compares each packet with its first numeric value
def cmp_first_num(l, r) -> int:
    while isinstance(l, list):
        l = l[0] if len(l) > 0 else -1
    while isinstance(r, list):
        r = r[0] if len(r) > 0 else -1

    return -1 if l < r else 1


# end_cmp_first_num


def parse_packets(lines: list[str]):
    score = 0
    packets = [[[2]], [[6]]]

    for i in range(0, len(lines), 3):
        l = eval(lines[i].strip())
        r = eval(lines[i + 1].strip())
        packets.append(l)
        packets.append(r)

        if check_packets(l, r):
            score += (i // 3) + 1

    cmp = cmp_to_key(lambda x, y: cmp_first_num(x, y))
    packets.sort(key=cmp)

    i2 = packets.index([[2]]) + 1
    i6 = packets.index([[6]]) + 1

    print(f"Pt 1: {score}")
    print(f"Pt 2: {i2 * i6}")


# end_parse_packets


if __name__ == "__main__":
    lines = get_lines("input.txt")
    parse_packets(lines)
