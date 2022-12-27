from .graph_data import GraphData


class GraphElementView:
    '''A base graph core data view.'''

    _graph_data = None
    _vertices_data = None
    _edges_data = None

    def link_to_graph(self, graph: GraphData):
        self._graph_data = graph
        self._vertices_data = graph.vertices_data
        self._edges_data = graph.edges_data
        return self

    def __hash__(self) -> int:
        return hash(self.get_source_data())

    def __eq__(self, other) -> int:
        return hash(self) == hash(other)

    def get_source_data(self):
        raise NotImplementedError()


class UsesGraphView:

    _graph = None

    def use_interface(self, graph_view) -> None:
        self._graph = graph_view
