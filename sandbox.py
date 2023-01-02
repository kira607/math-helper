from math_helper.graph import DiGraph


class DotAttrsCollection:
    pass


class VertexDot:

    def __call__(self) -> str:
        '''render dot string.'''
        return self._render()

    def set_attrs(self):
        '''set dot attributes'''

    def get_attrs(self):
        '''get dot attributes.'''

    def _render(self):
        return ''


def main() -> None:
    g = DiGraph()
    g.graph_attrs = {'a': 'b'}
    g.add_edge(2, 1).bidirectional = True
    g.add_edge(3, 4)
    edge = g.add_edge(1, 4)
    edge.v1.model.attrs = {'shape': 'diamond'}
    print(edge.v1.model.attrs)
    edge.model.attrs = {'color': 'red'}
    print(g.dot())
    print(g.get_edge(1, 2) == g.get_edge(2, 1))


if __name__ == '__main__':
    main()
