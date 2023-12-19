import copy
import re


def get_lines(filename: str):
    lines = []

    f = open(filename, "r")
    for line in f:
        lines.append(line.strip())

    f.close()
    return lines


pt2 = 0


def parse_workflow(line: str):
    global pt2
    pattern = r"(\w+){(.*)}"
    m = re.match(pattern, line)
    if m is None:
        return
    name, checks = m.group(1), m.group(2)
    chks, default = checks.split(",")[:-1], checks.split(",")[-1]

    chks = list(
        map(lambda chk: {"cmp": chk.split(":")[0], "then": chk.split(":")[1]}, chks)
    )

    return {"name": name, "else": default, "checks": chks}


def get_part_sum(line: str):
    pattern = r"{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}"
    m = re.match(pattern, line)
    if m is None:
        return 0
    x, m, a, s = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))
    return x + m + a + s


def parse_part(line: str, wf_dict, wf_name):
    if wf_name == "A":
        return True
    elif wf_name == "R":
        return False

    pattern = r"{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}"
    m = re.match(pattern, line)
    if m is None:
        return
    x, m, a, s = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))

    wf = wf_dict[wf_name]

    for check in wf["checks"]:
        if eval(check["cmp"]):
            return parse_part(line, wf_dict, check["then"])
    return parse_part(line, wf_dict, wf["else"])


def parse_part2(wf_dict, wf_name, vals):
    global pt2
    n_vals = copy.deepcopy(vals)
    x, m, a, s = n_vals
    if wf_name == "A":
        dx = x[1] - x[0] + 1
        dm = m[1] - m[0] + 1
        da = a[1] - a[0] + 1
        ds = s[1] - s[0] + 1
        s = dx * dm * da * ds
        pt2 += s
        return
    elif wf_name == "R":
        return

    wf = wf_dict[wf_name]
    for check in wf["checks"]:
        cmp = check["cmp"]
        cmp_val = int((cmp.split("<") if "<" in cmp else cmp.split(">"))[1])

        if cmp[0] == "x":
            tmp_x = x[:]
            if cmp[1] == "<":
                tmp_x[1] = min(cmp_val - 1, x[1])
                x[0] = min(cmp_val, x[1])
            elif cmp[1] == ">":
                tmp_x[0] = max(cmp_val + 1, x[0])
                x[1] = max(cmp_val, x[0])
            if tmp_x[0] > tmp_x[1]:
                return
            parse_part2(wf_dict, check["then"], [tmp_x, m, a, s])

        if cmp[0] == "m":
            tmp_m = m[:]
            if cmp[1] == "<":
                tmp_m[1] = min(cmp_val - 1, m[1])
                m[0] = min(cmp_val, m[1])
            elif cmp[1] == ">":
                tmp_m[0] = max(cmp_val + 1, m[0])
                m[1] = max(cmp_val, m[0])
            if tmp_m[0] > tmp_m[1]:
                return
            parse_part2(wf_dict, check["then"], [x, tmp_m, a, s])

        if cmp[0] == "a":
            tmp_a = a[:]
            if cmp[1] == "<":
                tmp_a[1] = min(cmp_val - 1, a[1])
                a[0] = min(cmp_val, a[1])
            elif cmp[1] == ">":
                tmp_a[0] = max(cmp_val + 1, a[0])
                a[1] = max(cmp_val, a[0])
            if tmp_a[0] > tmp_a[1]:
                return
            parse_part2(wf_dict, check["then"], [x, m, tmp_a, s])

        if cmp[0] == "s":
            tmp_s = s[:]
            if cmp[1] == "<":
                tmp_s[1] = min(cmp_val - 1, s[1])
                s[0] = min(cmp_val, s[1])
            elif cmp[1] == ">":
                tmp_s[0] = max(cmp_val + 1, s[0])
                s[1] = max(cmp_val, s[0])
            if tmp_s[0] > tmp_s[1]:
                return
            parse_part2(wf_dict, check["then"], [x, m, a, tmp_s])

    parse_part2(wf_dict, wf["else"], [x, m, a, s])
    pass


def solve(lines: list[str]):
    global pt2
    pt1 = 0
    half2 = False

    wf_dict = {}

    for line in lines:
        if line == "":
            half2 = True
            continue

        if not half2:
            wf = parse_workflow(line)
            if wf is not None:
                wf_dict[wf["name"]] = wf

        else:
            part_sum = get_part_sum(line)
            status = parse_part(line, wf_dict, "in")
            if status:
                pt1 += part_sum

    vals = [[1, 4000], [1, 4000], [1, 4000], [1, 4000]]
    parse_part2(wf_dict, "in", vals)

    print(f"Silver: {pt1}\nGold: {pt2}")


if __name__ == "__main__":
    lines = get_lines("input.txt")
    solve(lines)
