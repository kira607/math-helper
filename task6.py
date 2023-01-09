from base_task import BaseTask
from math_helper.graph import di_graph
from math_helper.graph.algorithms import KosarajuAlgorithm


class Task6(BaseTask):
    def _solve(self) -> None:
        g = di_graph(list(iter('ABCDEFGHIJKLMNOP')))
        g.add_edge('B', 'C')
        g.add_edge('A', 'E')
        g.add_edge('B', 'E').bidirectional = True
        g.add_edge('C', 'E').bidirectional = True
        g.add_edge('C', 'F')
        g.add_edge('C', 'G')
        g.add_edge('D', 'H')
        g.add_edge('E', 'F')
        g.add_edge('F', 'G')
        g.add_edge('E', 'K')
        g.add_edge('F', 'K').bidirectional = True
        g.add_edge('G', 'K')
        g.add_edge('I', 'J').bidirectional = True
        g.add_edge('J', 'K')
        g.add_edge('M', 'I')
        g.add_edge('P', 'O')
        g.add_edge('P', 'I')
        g.add_edge('P', 'J')
        g.add_edge('P', 'K').bidirectional = True
        g.add_edge('P', 'G')
        g.add_edge('P', 'C').bidirectional = True
        g.add_edge('L', 'C')

        print(g.dot())

        components = KosarajuAlgorithm.get_strongly_connected_components(g)
        for c in components:
            print(c.dot())


def solve() -> None:
    Task6(6).solve()


if __name__ == '__main__':
    solve()
