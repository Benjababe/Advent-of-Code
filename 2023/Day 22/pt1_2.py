import re
from collections import defaultdict
from dataclasses import dataclass


@dataclass
class Coord:
    x: int
    y: int
    z: int


@dataclass
class Brick:
    id: int
    start: Coord
    end: Coord
    vol: int
    height: int
    bottom: int
    x_rng: range
    y_rng: range


brick_map = defaultdict(lambda: -1)
supporting_dict = defaultdict(lambda: set([]))
supported_by_dict = defaultdict(lambda: set([]))
disintegratable = set([])
to_collapse = set()


def get_lines(filename: str):
    lines = []

    f = open(filename, "r")
    for line in f:
        lines.append(line)

    f.close()
    return lines


def get_bricks(lines: list[str]) -> list[Brick]:
    bricks = []
    pattern = r"(\d+,\d+,\d+)~(\d+,\d+,\d+)"

    for line in lines:
        match = re.match(pattern, line.strip())
        if match is None:
            continue
        xyz1, xyz2 = match.group(1), match.group(2)
        xyz1 = [int(n) for n in xyz1.split(",")]
        xyz2 = [int(n) for n in xyz2.split(",")]

        start = Coord(xyz1[0], xyz1[1], xyz1[2])
        end = Coord(xyz2[0], xyz2[1], xyz2[2])
        vol = (
            (xyz2[0] - xyz1[0] + 1) * (xyz2[1] - xyz1[1] + 1) * (xyz2[2] - xyz1[2] + 1)
        )
        bottom = min(xyz1[2], xyz2[2])
        x_rng = range(min(xyz1[0], xyz2[0]), max(xyz1[0], xyz2[0]) + 1)
        y_rng = range(min(xyz1[1], xyz2[1]), max(xyz1[1], xyz2[1]) + 1)
        height = abs(xyz1[2] - xyz2[2]) + 1

        bricks.append(Brick(len(bricks), start, end, vol, height, bottom, x_rng, y_rng))

    bricks.sort(key=lambda b: b.bottom)

    return bricks


def brick_fall(bricks: list[Brick]):
    global brick_map

    for idx, brick in enumerate(bricks):
        if idx == 6:
            pass

        while brick.bottom > 1:
            can_fall = True

            for x in brick.x_rng:
                for y in brick.y_rng:
                    key = (x, y, brick.bottom - 1)
                    if (
                        key in brick_map
                        and brick_map[key] != -1
                        and brick_map[key] != brick.id
                    ):
                        can_fall = False

            if can_fall:
                brick.bottom -= 1
            else:
                break

        for x in brick.x_rng:
            for y in brick.y_rng:
                for h in range(brick.height):
                    brick_map[(x, y, brick.bottom + h)] = brick.id

        bricks[idx] = brick

    return bricks


def get_disintegrate(bricks: list[Brick]) -> int:
    global brick_map, supporting_dict, supported_by_dict, disintegratable

    support_count = defaultdict(lambda: set())
    support_by_count = defaultdict(lambda: set())

    for brick in bricks[::-1]:
        supports = set()
        for x in brick.x_rng:
            for y in brick.y_rng:
                key = (x, y, brick.bottom - 1)
                if (
                    key in brick_map
                    and brick_map[key] != -1
                    and brick_map[key] != brick.id
                ):
                    supports.add(brick_map[key])
                    support_by_count[brick.id].add(brick_map[key])
                    support_count[brick_map[key]].add(brick.id)

        supported_by_dict[brick.id] = supports

        # check if brick supports any
        supporting = set()

        for x in brick.x_rng:
            for y in brick.y_rng:
                key = (x, y, brick.bottom + brick.height)
                if key in brick_map and brick_map[key] != -1:
                    supporting.add(brick_map[key])

        if len(supporting) == 0:
            disintegratable.add(brick.id)
        else:
            supporting_dict[brick.id] = supporting

    for id, support in support_count.items():
        only_support = set()
        for brick_id in support:
            if len(support_by_count[brick_id]) == 1:
                only_support.add(brick_id)

        if len(only_support) == 0:
            disintegratable.add(id)

    return len(disintegratable)


def check_upwards(master: int, brick_id: int) -> set:
    global brick_map, supporting_dict, supported_by_dict, disintegratable, to_collapse

    # check if everything below has fallen
    supported_by = supported_by_dict[brick_id]
    supported_by_in_die = to_collapse.intersection(supported_by)

    s = set()

    # if has, propagate forward
    if len(supported_by) == len(supported_by_in_die):
        s.add(brick_id)
        to_collapse = to_collapse.union([brick_id])
        supporting = supporting_dict[brick_id]

        for up_brick in supporting:
            more_bricks = check_upwards(master, up_brick)
            s = s.union(more_bricks)

    return s


def get_score(lines: list[str]):
    global brick_map, supporting_dict, supported_by_dict, disintegratable, to_collapse

    p1, p2 = 0, 0

    bricks = get_bricks(lines)
    bricks = brick_fall(bricks)
    p1 = get_disintegrate(bricks)

    for brick in bricks:
        if brick.id in disintegratable:
            continue
        s = set()
        to_collapse = set([brick.id])
        for up_brick in supporting_dict[brick.id]:
            next_s = check_upwards(brick.id, up_brick)
            s.union(next_s)
        p2 += len(to_collapse) - 1

    print(f"Silver: {p1}\nGold: {p2}")


if __name__ == "__main__":
    lines = get_lines("input.txt")
    get_score(lines)
