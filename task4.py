from base_task import BaseTask
from math_helper.graph import tree
from math_helper.graph.algorithms import PruferSerializer
from math_helper.graph.helpers import get_latex_tikz_string


class Task4(BaseTask):
    def _solve(self) -> None:
        g = tree()
        g.init_from_edges(
            (1, 7),
            (1, 8),
            (1, 9),
            (2, 9),
            (2, 10),
            (3, 4),
            (4, 5),
            (5, 6),
            (5, 10),
            (10, 11),
        )
        g.set_root(5)
        g.update_node_attrs({'shape': 'box'})
        g.root.update_dot_attrs({'color': 'blue'})
        print(g.dot())

        solution_steps = enumerate(PruferSerializer.serialize_by_steps(g.copy()), start=1)
        for step_n, (current_tree, min_leaf, parent, code) in solution_steps:
            print(f'\\textbf{{Шаг {step_n}}}\n')

            print('Граф:')
            min_leaf.update_dot_attrs({'color': 'red'})
            parent.update_dot_attrs({'color': 'green'})
            print(get_latex_tikz_string(current_tree))
            parent.update_dot_attrs({'color': 'black'})
            current_tree.get_node('5').update_dot_attrs({'color': 'blue'})

            print(f'Лист дерева с минимальным номером: {min_leaf.name}\n')
            print(f'Добавляем номер родителя минимального листа ({min_leaf.name}) '
                  f'в код и убираем минимальный лист из графа.\n')
            print(f'Код: {", ".join([str(c) for c in code])}\n')

        print(f'Полученный код: {PruferSerializer.serialize(g)}')


def solve() -> None:
    Task4(4).solve()


if __name__ == '__main__':
    solve()
