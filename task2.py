from base_task import BaseTask
from math_helper.graph import di_graph


def prefix(vertex):
    return vertex.name[:-1]


def suffix(vertex):
    return vertex.name[1:]


def word(edge):
    return edge.v1.name[0] + suffix(edge.v1) + edge.v2.name[-1]


class Task2(BaseTask):
    def _solve(self) -> None:
        g = di_graph('KQS, QSU, UQS, SQU, SUQ, QSQ, QUQ, UQU'.split(', '))

        for v1 in g.vertices:
            for v2 in g.vertices:
                if v1 == v2 or suffix(v1) != prefix(v2):
                    continue
                new_edge = g.add_edge(v1.name, v2.name)
                new_edge.update_dot_attrs({'label': word(new_edge)})

        print('resulting graph:')
        print(g.dot())
        print('words: ')
        print(',\n'.join(word(edge) for edge in g.edges), '.', sep='')


def solve() -> None:
    Task2(2).solve()


if __name__ == '__main__':
    solve()
