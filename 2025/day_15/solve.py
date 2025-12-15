import time


def format_time(sec: float) -> str:
    if sec < 0.001:
        return f"{sec * 1_000_000:.2f} microseconds"
    elif sec < 1:
        return f"{sec * 1000:.2f} milliseconds"
    else:
        return f"{sec:.2f} seconds"


def get_line(filename: str):
    f = open(filename, "r")
    line = f.read().strip()
    f.close()
    return line


def run_instructions(line: str):
    matching = {}
    st = []
    for i, char in enumerate(line):
        if char == "[":
            st.append(i)
        if char == "]":
            j = st.pop()
            matching[i] = j
            matching[j] = i

    mem = [0 for _ in range(6)]
    prev_l_bracket, prev_state = -1, mem.copy()
    i, cell = 0, 0
    while i < len(line):
        char = line[i]

        match char:
            case "+":
                mem[cell] += 1
            case "-":
                mem[cell] -= 1
            case "<":
                cell -= 1
            case ">":
                cell += 1
            case "[":
                if prev_l_bracket == i:
                    diff = {}
                    for j, v in enumerate(prev_state):
                        diff[j] = v - mem[j]

                    times = int(mem[cell] / diff[cell])
                    for k, v in diff.items():
                        mem[k] -= v * times
                else:
                    prev_l_bracket = i
                    prev_state = mem.copy()

                if mem[cell] == 0:
                    i = matching[i]
            case "]":
                i = matching[i] - 1
            case ".":
                print(f"Value of cell #{cell}: {mem[cell]}")

        i += 1


if __name__ == "__main__":
    line = get_line("input.txt")
    t1 = time.perf_counter()
    run_instructions(line)
    t2 = time.perf_counter()
    print(f"Time taken: {format_time(t2-t1)}")
