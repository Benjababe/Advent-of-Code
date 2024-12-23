import networkx as nx


def get_lines(filename: str):
    lines = []

    f = open(filename, "r")
    for line in f:
        lines.append(line.strip())

    f.close()
    return lines


def solve_p1(lines: list[str]) -> int:
    score = 0
    graph = nx.Graph()
    for line in lines:
        n1, n2 = line.split("-")
        graph.add_edge(n1, n2)

    for clique in nx.enumerate_all_cliques(graph):
        if len(clique) == 3 and any(node[0] == "t" for node in clique):
            score += 1

    return score


def solve_p2(lines: list[str]) -> str:
    graph = nx.Graph()
    for line in lines:
        n1, n2 = line.split("-")
        graph.add_edge(n1, n2)

    largest_clique = max(nx.find_cliques(graph), key=len)
    return ",".join(sorted([n for n in largest_clique]))


if __name__ == "__main__":
    lines = get_lines("input.txt")

    t_comps = solve_p1(lines)
    print(f"t_comps: {t_comps}")

    password = solve_p2(lines)
    print(f"Password: {password}")
