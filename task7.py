from base_task import BaseTask
from math_helper.graph import nd_graph, di_graph
from math_helper.graph.algorithms import find_euler_path
from math_helper.graph.helpers import get_latex_tikz_string


class Task7(BaseTask):
    def _solve(self) -> None:
        source = (
            '011000000',
            '101000110',
            '110110000',
            '001010000',
            '001101010',
            '000010111',
            '010001011',
            '010011100',
            '000001100',
        )
        matrix = [
            list(map(int, iter(line)))
            for line in source
        ]
        print(*matrix, sep='\n')

        vertices_list = [f'v_{{{i}}}' for i in range(len(matrix))]

        g = nd_graph(vertices_list)
        for v1, matrix_row in zip(g.vertices, matrix):
            for v2, connected in zip(g.vertices, matrix_row):
                if connected:
                    g.add_edge(v1.name, v2.name)

        print(g.dot())
        print(get_latex_tikz_string(g))

        print(sum(vertex.degree for vertex in g))
        print(len(tuple(g.edges)))

        euler_path = find_euler_path(g)

        g2 = di_graph(vertices_list)

        for i, v1 in enumerate(euler_path):
            if i == len(euler_path) - 1:
                break
            if i == 0:
                g2.get_vertex(v1).update_dot_attrs({'color': 'blue'})
            edge = g2.add_edge(v1, euler_path[i+1])
            edge.update_dot_attrs({'label': f'{i + 1}'})

        print(g2.dot())


def solve() -> None:
    Task7(7).solve()


if __name__ == '__main__':
    solve()
