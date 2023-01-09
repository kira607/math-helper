from typing import Iterable

from math_helper.graph.common import BaseGraph, GraphVertexView
from math_helper.graph.common.dot_bundle import EdgeViewWithDot
from math_helper.utils.types import StrConvertable


class DiGraphVertexView(GraphVertexView):

    @property
    def in_edges(self) -> list['DiGraphEdgeView']:
        edges = []
        for incident_edge in self.incident_edges:
            if incident_edge.v2.name == self.name:
                edges.append(incident_edge)

        return edges

    @property
    def out_edges(self) -> list['DiGraphEdgeView']:
        edges = []
        for incident_edge in self.incident_edges:
            if incident_edge.v1.name == self.name:
                edges.append(incident_edge)

        return edges

    @property
    def in_vertices(self) -> list['DiGraphVertexView']:
        return [edge.v1 for edge in self.in_edges]

    @property
    def out_vertices(self) -> list['DiGraphVertexView']:
        return [edge.v2 for edge in self.out_edges]

    @property
    def in_degree(self) -> int:
        return sum(1 for _ in self.in_edges)

    @property
    def out_degree(self) -> int:
        return sum(1 for _ in self.out_edges)


class DiGraphEdgeView(EdgeViewWithDot):

    @property
    def bidirectional(self) -> bool:
        edge_data = self._gc.edges_data[self._v1][self._v2]
        return edge_data.bidirectional

    @bidirectional.setter
    def bidirectional(self, bidirectional: bool) -> None:
        edge_model = self._gc.edges_data[self._v1][self._v2]
        edge_model.bidirectional = bidirectional
        edge_model.dot_attrs['dir'] = 'both' if bidirectional else 'one'
        v1, v2 = self.v1.name, self.v2.name
        self._gc.edges_data[v2][v1] = edge_model if bidirectional else None

    def set_direction(self, target: str) -> None:
        v1, v2 = self._v1, self._v2
        this_vertices = v1, v2
        if target not in this_vertices:
            raise ValueError(f'target must be one of: {this_vertices}. Got: {target}')

        edge_data = self._gc.edges_data[self._v1][self._v2]
        edge_data.bidirectional = False

        if target == v1:
            self._gc.edges_data[v1][v2] = None
            self._v1, self._v2 = self._v2, self._v1
        elif target == v2:
            self._gc.edges_data[v2][v1] = None

    def flip_direction(self) -> None:
        if self.bidirectional:
            return

        v1, v2 = self._v1, self._v2
        em = self._gc.edges_data[self._v1][self._v2]

        self._gc.edges_data[v2][v1] = em
        self._gc.edges_data[v1][v2] = None
        self._v1, self._v2 = self._v2, self._v1


class DiGraphView(BaseGraph):

    def add_edge(self, v1: StrConvertable, v2: StrConvertable):
        new_edge = self._gc.add_edge(v1, v2)
        return new_edge

    def remove_edge(self, v1: StrConvertable, v2: StrConvertable) -> None:
        self._gc.remove_edge(v1, v2)
        self._gc.remove_edge(v2, v1)

    def merge_edge(self, v1: StrConvertable, v2: StrConvertable, to_remove: StrConvertable = None):
        self._gc.merge_edge(v1, v2, to_remove)

    def get_sub_graph(self, sub_vertices: Iterable[StrConvertable]):
        return self._gc.get_sub_graph(sub_vertices)

    @property
    def transpose(self) -> 'DiGraphView':
        return self._gc.get_transpose()
