from typing import Any
from typing import Generator

from math_helper.graph.core.views import EdgeView
from math_helper.utils import MISSING
from math_helper.utils.types import StrConvertable

from .dot_bundle import GraphViewWithDot
from .dot_bundle import VertexViewWithDot


class BaseGraph(GraphViewWithDot):
    '''A base graph model view.'''

    def __iter__(self):
        return iter(self.vertices)

    @property
    def vertices(self):
        return iter(self._gc.vertices)

    @property
    def edges(self):
        return iter(self._gc.edges)

    @property
    def vertices_count(self) -> int:
        return self._gc.vertices_count

    @property
    def edges_count(self) -> int:
        return self._gc.edges_count

    def get_vertex(self, vertex_name: StrConvertable, default: Any = MISSING):
        return self._gc.get_vertex(vertex_name, default)

    def add_vertex(self, vertex_name: StrConvertable):
        return self._gc.add_vertex(vertex_name)

    def remove_vertex(self, vertex_name: StrConvertable):
        self._gc.remove_vertex(vertex_name)

    def get_edge(self, v1: StrConvertable, v2: StrConvertable, default: Any = MISSING):
        return self._gc.get_edge(v1, v2, default)


class GraphVertexView(VertexViewWithDot):

    @property
    def adjacent_vertices(self) -> Generator['GraphVertexView', None, None]:
        for e in self._gc.pair_matches(self._name, True):
            yield self._gc.get_vertex(e.v2.name)

    @property
    def incident_edges(self) -> Generator[EdgeView, None, None]:
        for e in self._gc.pair_matches(self._name, True):
            yield e

    @property
    def degree(self) -> int:
        return len(tuple(self.incident_edges))
