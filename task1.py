from base_task import BaseTask
from math_helper.graph.algorithms import get_radius, get_diameter, get_centers
from math_helper.graph import nd_graph


class Task1(BaseTask):
    def _solve(self) -> None:
        g = nd_graph(edges=[
            ('2', '3'),
            ('4', '5'),
            ('1', '6'),
            ('2', '6'),
            ('4', '6'),
            ('4', '7'),
            ('4', '9'),
            ('5', '10'),
            ('8', '9'),
        ])

        print(g.dot())
        print(f'{get_radius(g)=}')
        print(f'{get_diameter(g)=}')
        print(f'{get_centers(g)=}')


def solve() -> None:
    Task1(1).solve()


if __name__ == '__main__':
    solve()
