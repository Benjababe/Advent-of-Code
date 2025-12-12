import platform
import subprocess
import time


DIRECTIONS = [
    (0, 0, -1),
    (0, 0, 1),
    (0, -1, 0),
    (0, 1, 0),
    (-1, 0, 0),
    (1, 0, 0),
]


def format_time(sec: float) -> str:
    if sec < 0.001:
        return f"{sec * 1_000_000:.2f} microseconds"
    elif sec < 1:
        return f"{sec * 1000:.2f} milliseconds"
    else:
        return f"{sec:.2f} seconds"


def get_layers(filename: str):
    layers = []

    f = open(filename, "r")
    for layer in f.read().split("\n\n"):
        layers.append(layer.strip())

    f.close()
    return layers


def get_score(layers: list[str], pt2: bool) -> int:
    size = len(layers)
    cavern = [layer.split() for layer in layers]

    queue = [(x, y, 0) for x in range(size) for y in range(size) if cavern[0][y][x] == "."]
    visited: set[tuple[int, int, int]] = set()
    ice: set[tuple[int, int, int]] = set()
    while len(queue) > 0:
        x, y, z = queue.pop(0)
        if (x, y, z) in visited:
            continue
        visited.add((x, y, z))

        for (dx, dy, dz) in DIRECTIONS:
            nx, ny, nz = x+dx, y+dy, z+dz
            if not (0 <= nx < size and 0 <= ny < size and 0 <= nz < size):
                continue

            if cavern[nz][ny][nx] == ".":
                queue.append((nx, ny, nz))
            else:
                ice.add((nx, ny, nz))
    if not pt2:
        return len(ice)

    trapped_air = 0
    for z in range(size):
        for y in range(size):
            for x in range(size):
                if cavern[z][y][x] == "." and (x, y, z) not in visited:
                    trapped_air += 1

    return trapped_air


if __name__ == "__main__":
    layers = get_layers("input.txt")

    t1 = time.perf_counter()
    score_pt1 = get_score(layers, False)
    t2 = time.perf_counter()
    print(f"Score Pt1: {score_pt1}\tTime taken: {format_time(t2-t1)}")

    t1 = time.perf_counter()
    score_pt2 = get_score(layers, True)
    t2 = time.perf_counter()
    print(f"Score Pt2: {score_pt2}\tTime taken: {format_time(t2-t1)}")

    # Remove if unnecessary
    if platform.system() == "Windows":
        subprocess.run("clip", text=True, input=str(score_pt1))
    elif platform.system() == "Darwin":
        subprocess.run("pbcopy", text=True, input=str(score_pt1))
    elif platform.system() == "Linux":
        subprocess.run(
            "xclip -selection clipboard", text=True, input=str(score_pt1), shell=True
        )
    print(f"{score_pt1} copied to the clipboard")
