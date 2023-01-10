from math_helper.graph import flow_network
from math_helper.graph.algorithms import EdmondsKarpAlgorithm


class BaseTask:

    def __init__(self, number: int) -> None:
        self.number = number

    def solve(self) -> None:
        print(f'#### TASK №{self.number} SOLUTION ####')
        self._solve()

    def _solve(self) -> None:
        raise NotImplementedError()


class Task(BaseTask):
    def _solve(self) -> None:
        vertices_list = list(iter('ABCDEFGHIJKLMN'))
        g = flow_network(vertices_list)
        g.add_edge('A', 'B').capacity = 21
        g.add_edge('A', 'C').capacity = 19
        g.add_edge('A', 'D').capacity = 10
        g.add_edge('B', 'E').capacity = 4
        g.add_edge('B', 'F').capacity = 6
        g.add_edge('C', 'E').capacity = 8
        g.add_edge('C', 'G').capacity = 4
        g.add_edge('D', 'F').capacity = 10
        g.add_edge('D', 'G').capacity = 1
        g.add_edge('E', 'H').capacity = 4
        g.add_edge('E', 'I').capacity = 9
        g.add_edge('F', 'H').capacity = 10
        g.add_edge('F', 'J').capacity = 5
        g.add_edge('G', 'I').capacity = 7
        g.add_edge('G', 'J').capacity = 10
        g.add_edge('H', 'K').capacity = 5
        g.add_edge('H', 'L').capacity = 2
        g.add_edge('I', 'K').capacity = 6
        g.add_edge('I', 'M').capacity = 8
        g.add_edge('J', 'L').capacity = 2
        g.add_edge('J', 'M').capacity = 2
        g.add_edge('K', 'N').capacity = 19
        g.add_edge('L', 'N').capacity = 14
        g.add_edge('M', 'N').capacity = 21

        g.source = 'A'
        g.sink = 'N'

        for edge in g.edges:
            edge.update_dot_attrs({'label': edge.capacity})

        print(g.dot())

        print(EdmondsKarpAlgorithm.get_max_flow(g))


def solve() -> None:
    Task(0).solve()


if __name__ == '__main__':
    solve()
