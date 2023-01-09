from math_helper.graph.common import BaseGraph
from math_helper.graph.common.dot_bundle import EdgeViewWithDot
from math_helper.graph.digraph.views import DiGraphVertexView
from math_helper.utils.types import StrConvertable


class FNVertexView(DiGraphVertexView):
    pass


class FNEdgeView(EdgeViewWithDot):

    @property
    def capacity(self) -> float:
        edge = self._gc.edges_data.get(self._v1, self._v2)
        return edge.capacity

    @capacity.setter
    def capacity(self, new_capacity: float) -> None:
        edge = self._gc.edges_data.get(self._v1, self._v2)
        edge.capacity = new_capacity


class FNView(BaseGraph):

    @property
    def source(self) -> FNVertexView | None:
        return self._gc.get_vertex(self._gc.graph_model.source, None)

    @property
    def sink(self) -> FNVertexView | None:
        return self._gc.get_vertex(self._gc.graph_model.sink, None)

    def add_edge(self, v1: StrConvertable, v2: StrConvertable):
        new_edge = self._gc.add_edge(v1, v2)
        return new_edge

    def remove_edge(self, v1: StrConvertable, v2: StrConvertable) -> None:
        self._gc.remove_edge(v1, v2)
        self._gc.remove_edge(v2, v1)
