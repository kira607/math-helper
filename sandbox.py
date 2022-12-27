from math_helper.graph import DiGraph
from math_helper.graph.dot import DiGraphDotRenderer


def main() -> None:
    g = DiGraph()
    g.add_edge(2, 1).bidirectional = True
    g.add_edge(3, 4)
    g.add_edge(1, 4)
    print(DiGraphDotRenderer(g).render())
    print(g.get_edge(1, 2) == g.get_edge(2, 1))


if __name__ == '__main__':
    main()
