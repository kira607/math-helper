from base_task import BaseTask
from math_helper.graph import di_graph
from math_helper.graph.algorithms import ChromaticPolynomCreator


class Task3(BaseTask):
    def _solve(self) -> None:
        g = di_graph(edges=[
            ('A', 'B'),
            ('B', 'D'),
            ('C', 'D'),
            ('D', 'E'),
            ('C', 'H'),
            ('D', 'H'),
            ('E', 'I'),
            ('E', 'J'),
            ('F', 'J'),
            ('G', 'H'),
            ('H', 'I'),
            ('H', 'K'),
            ('I', 'K'),
            ('K', 'L'),
        ])
        print(g.dot())
        print(ChromaticPolynomCreator.get_chromatic_polynom(g))


def solve() -> None:
    Task3(3).solve()


if __name__ == '__main__':
    solve()
