import copy

best_queue = []
max_pressure = 0

memoi = {}


def get_lines(filename: str):
    lines = []

    f = open(filename, "r")
    for line in f:
        lines.append(line)

    f.close()
    return lines
# end_get_lines


def get_dist(d_valves: dict, source: str, dest: str) -> dict:
    queue = [[source]]
    visited = []

    while len(queue) > 0:
        path = queue.pop(0)
        visited.append(path[-1])

        if path[-1] == dest:
            return {"path": path[1:], "dist": len(path)-1}

        neighbours = d_valves[path[-1]]["neighbours"]

        for n in neighbours:
            if n not in visited:
                tmp = path.copy()
                tmp.append(n)
                queue.append(tmp)

    return {"path": [], "dist": 0}


# find weighted distance to its neighbours
def clean_valves(d_valves: dict, valves: dict):
    for v in valves:
        neighbours = valves[v]["neighbours"]

        for n in neighbours:
            valves[v]["neighbours"][n] = get_dist(d_valves, v, n)


def check_all_valves_turned(valves):
    all_closed = True

    for v in valves:
        if valves[v]["turned"] == False:
            return False

    return True


def traverse(valves: dict, path: list[str], p_sum: int, time: int) -> int:
    global max_pressure, best_queue

    if p_sum < 1000 and time <= 10:
        return 0

    if ",".join(path) in memoi and memoi[",".join(path)] > p_sum:
        return 0

    if time <= 0:
        return 0

    cur_valve = path[-1].split("*")[0] if "*" in path[-1][-1] else path[-1]
    v = valves[cur_valve]

    i_path = copy.deepcopy(path)

    if check_all_valves_turned(valves):
        return 0

    options = [0]
    if v["flow_rate"] > 0 and v["turned"] == False:
        options.append(1)

    if 1 in options:
        tmp_valves = copy.deepcopy(valves)
        tmp_valves[cur_valve]["turned"] = True
        time -= 1
        tmp_sum = p_sum + (time * tmp_valves[cur_valve]["flow_rate"])

        if tmp_sum > max_pressure:
            max_pressure = tmp_sum
            best_queue = i_path.copy()
            print(max_pressure)
            print(best_queue)
            print()

        memoi[",".join(i_path)] = tmp_sum

        for n in v["neighbours"]:
            if (len(i_path) > 2 and i_path[-2] == n) or tmp_valves[n]["turned"] == True:
                continue
            else:
                tmp_path = i_path.copy() + [n]
                dist = v["neighbours"][n]["dist"]
                traverse(tmp_valves, tmp_path, tmp_sum, time-dist)

    if 0 in options:
        tmp_valves = copy.deepcopy(valves)
        for n in v["neighbours"]:
            if (len(path) > 2 and path[-2] == n) or tmp_valves[n]["turned"] == True:
                continue
            else:
                tmp_path = path.copy() + [n]
                tmp_valves = copy.deepcopy(valves)
                dist = v["neighbours"][n]["dist"]
                traverse(tmp_valves, tmp_path, p_sum, time-dist)

    return 0


def get_score(lines: list[str]) -> int:
    score = 0
    i = 0
    dirty_valves = {}
    good_valves = {}

    for line in lines:
        v, t = line.strip().split(";")
        valve, flow_rate = v.split("=")
        valve = valve.split()[1]

        t = t.split("valves" if "valves" in t else "valve")[1]
        tunnels = t.split(",")
        tunnels = [t.strip() for t in tunnels]
        tunnels = sorted(tunnels)

        dirty_valves[valve] = {
            "turned": False,
            "flow_rate": int(flow_rate),
            "neighbours": tunnels
        }

        if int(flow_rate) > 0:
            good_valves[valve] = {
                "turned": False,
                "flow_rate": int(flow_rate)
            }

        if valve == "AA":
            good_valves["AA"] = {
                "turned": True,
                "flow_rate": int(flow_rate)
            }

    for v in good_valves:
        good_valves[v]["neighbours"] = dict(
            [(i, {}) for i in good_valves if i != v and i != "AA"])

    clean_valves(dirty_valves, good_valves)

    path = ["AA"]
    score = traverse(good_valves, path, 0, 30)

    return score
# end_get_score


if __name__ == "__main__":
    lines = get_lines("input.txt")
    score = get_score(lines)

    print(f"Score: {score}")
