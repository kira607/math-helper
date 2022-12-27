import math_helper.graph.base as base

from math_helper.utils import Typed


class DiEdge(base.Edge):

    bidirectional = Typed(bool)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.bidirectional = False

    def __str__(self) -> str:
        _dir = 'both' if self.bidirectional else 'one'
        _cls = self.__class__.__name__
        return f'{_cls}(v1={self.v1}, v2={self.v2}, dir={_dir})'


class DiEdgeView(base.EdgeView):

    @property
    def bidirectional(self) -> bool:
        edge_data = self.get_source_data()
        return edge_data.bidirectional

    @bidirectional.setter
    def bidirectional(self, bidirectional: bool) -> None:
        edge_data = self.get_source_data()
        edge_data.bidirectional = bidirectional
        v1, v2 = self.v1.name, self.v2.name
        self._edges_data[v2][v1] = edge_data if bidirectional else None

    def set_direction(self, target: str) -> None:
        v1, v2 = self.v1.name, self.v2.name
        this_vertices = v1, v2
        if target not in this_vertices:
            raise ValueError(f'target must be one of: {this_vertices}. Got: {target}')

        edge_data = self.get_source_data()
        edge_data.bidirectional = False

        if target == v2:
            self._edges_data[v2][v1] = None
        else:
            self._edges_data[v1][v2] = None


class DiGraph(base.Graph):

    _edge_data_type = DiEdge
    _edge_view_type = DiEdgeView

    def _add_edge(self, v1: str, v2: str) -> None:
        new_edge = self._make_edge_data(v1, v2)
        self._edges_data[v1][v2] = new_edge

    def _remove_edge(self, v1: str, v2: str) -> None:
        bidirectional = self._edges_data[v1][v2].bidirectional
        self._edges_data[v1][v2] = None
        if bidirectional:
            self._edges_data[v2][v1] = None
