from typing import Type

from math_helper.graph.common import GraphVertexView
from math_helper.graph.common.base_graph import BaseGraph
from math_helper.graph.models import EdgeModel
from math_helper.graph.models import VertexModel
from math_helper.graph.ndgraph import NdGraph
from math_helper.graph.views import EdgeView
from math_helper.graph.views import VertexView
from math_helper.utils import Typed
from math_helper.utils.types import StrConvertable


class DiGraphVertexView(GraphVertexView):

    @property
    def in_edges(self) -> list[EdgeView]:
        vertex = self.get_model()
        out_edges = []
        incident_edges = self.incident_edges

        for incident_edge in incident_edges:
            if incident_edge.v2.name == vertex.name:
                out_edges.append(incident_edge)

        return out_edges

    @property
    def out_edges(self) -> list[EdgeView]:
        vertex = self.get_model()
        in_edges = []
        incident_edges = self.incident_edges

        for incident_edge in incident_edges:
            if incident_edge.v1.name == vertex.name:
                in_edges.append(incident_edge)

        return in_edges

    @property
    def in_vertices(self) -> list['DiGraphVertexView']:
        edges = self.in_edges
        return [edge.v1 for edge in edges]

    @property
    def out_vertices(self) -> list['DiGraphVertexView']:
        edges = self.out_edges
        return [edge.v2 for edge in edges]

    @property
    def in_degree(self) -> int:
        in_edges = self.in_edges
        return len(in_edges)

    @property
    def out_degree(self) -> int:
        out_edges = self.out_edges
        return len(out_edges)


class DiEdgeModel(EdgeModel):

    bidirectional = Typed(bool)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.bidirectional = False

    def __str__(self) -> str:
        _dir = 'both' if self.bidirectional else 'one'
        _cls = self.__class__.__name__
        return f'{_cls}(v1={self.v1}, v2={self.v2}, dir={_dir})'


class DiEdgeView(EdgeView):

    @property
    def bidirectional(self) -> bool:
        edge_data = self.get_model()
        return edge_data.bidirectional

    @bidirectional.setter
    def bidirectional(self, bidirectional: bool) -> None:
        edge_data = self.get_model()
        edge_data.bidirectional = bidirectional
        v1, v2 = self.v1.name, self.v2.name
        self._edges_data[v2][v1] = edge_data if bidirectional else None

    def set_direction(self, target: str) -> None:
        v1, v2 = self._v1, self._v2
        this_vertices = v1, v2
        if target not in this_vertices:
            raise ValueError(f'target must be one of: {this_vertices}. Got: {target}')

        edge_data = self.get_model()
        edge_data.bidirectional = False

        if target == v1:
            self._edges_data[v1][v2] = None
            self._v1, self._v2 = self._v2, self._v1
        elif target == v2:
            self._edges_data[v2][v1] = None

    def flip_direction(self) -> None:
        if self.bidirectional:
            return

        v1, v2 = self._v1, self._v2
        em = self.get_model()

        self._edges_data[v2][v1] = em
        self._edges_data[v1][v2] = None
        self._v1, self._v2 = self._v2, self._v1


class DiGraph(BaseGraph):

    _vertex_model_type: Type[VertexModel] = VertexModel
    _vertex_view_type: Type[VertexView] = GraphVertexView
    _edge_model_type: Type[EdgeModel] = DiEdgeModel
    _edge_view_type: Type[EdgeView] = DiEdgeView

    def add_edge(self, v1: StrConvertable, v2: StrConvertable) -> _edge_view_type:
        new_edge = self._controller.add_edge(v1, v2)
        new_edge = new_edge.get_model()
        self._controller.put_edge(new_edge, v2, v1)
        return new_edge

    def remove_edge(self, v1: StrConvertable, v2: StrConvertable) -> None:
        self._controller.remove_edge(v1, v2)
        self._controller.remove_edge(v2, v1)  # we can safely remove flipped edge. no need for bidirectional check

    def get_transpose(self) -> 'DiGraph':
        transpose_model = self._graph_model.copy()
        for v1, col in transpose_model.edges_data.items():
            for v2, edge in col.items():
                edge.flip_direction()
        return DiGraph(transpose_model)
