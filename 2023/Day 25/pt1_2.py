import networkx as nx


def get_lines(filename: str):
    lines = []

    f = open(filename, "r")
    for line in f:
        lines.append(line)

    f.close()
    return lines


def get_score(lines: list[str]) -> int:
    score = 1
    g = nx.Graph()
    for line in lines:
        node, children = line.strip().split(":")
        for ch in [ch.strip() for ch in children.split()]:
            g.add_edge(node, ch)
    remove = list(nx.minimum_edge_cut(g))
    g.remove_edges_from(remove)
    for component in nx.connected_components(g):
        score *= len(component)

    return score


if __name__ == "__main__":
    lines = get_lines("input.txt")
    score = get_score(lines)
    print(f"Score: {score}")
