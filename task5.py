from base_task import BaseTask
from string import Template

from math_helper.graph import tree
from math_helper.graph.algorithms import PruferSerializer
from math_helper.graph.helpers import get_latex_tikz_string


def comma_join(items):
    return ', '.join((str(item) for item in items))


class Task5(BaseTask):
    def _solve(self) -> None:
        code = [7, 3, 3, 9, 3, 4, 4, 5, 6]
        step_template = Template('''
\\textbf{Шаг} $step_n

Код: $left_code

Оставшиеся вершины: $available_vertices

Оставшиеся вершины не входящие в код: $not_in_code

Минимальная оставшиеся вершина не входящяя в код: $v2

Новое ребро для добавления: $new_edge

Полученные рёбра: $edges
        ''')

        solution_steps = enumerate(PruferSerializer.deserialize_by_steps(code), start=1)
        for step_n, (left_code, available_vertices, not_in_code, v2, new_edge, edges) in solution_steps:
            print(step_template.substitute(
                step_n=step_n,
                left_code=comma_join(left_code),
                available_vertices=comma_join(available_vertices),
                not_in_code=comma_join(not_in_code),
                v2=v2,
                new_edge=new_edge,
                edges=comma_join(edges),
            ))

        print('Полученный граф:')
        t = tree()
        t.init_from_edges(*edges)
        print(get_latex_tikz_string(t))

        print(t.dot())


def solve() -> None:
    Task5(5).solve()


if __name__ == '__main__':
    solve()
