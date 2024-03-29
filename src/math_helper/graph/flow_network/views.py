from math_helper.graph.common import BaseGraph
from math_helper.graph.common.dot_bundle import EdgeViewWithDot
from math_helper.graph.digraph.views import DiGraphVertexView
from math_helper.utils.types import StrConvertable


class FNVertexView(DiGraphVertexView):
    pass


class FNEdgeView(EdgeViewWithDot):

    @property
    def capacity(self) -> int:
        edge = self._gc.edges_data.get(self._v1).get(self._v2)
        return edge.capacity

    @capacity.setter
    def capacity(self, new_capacity: int) -> None:
        edge = self._gc.edges_data.get(self._v1).get(self._v2)
        edge.capacity = new_capacity

    @property
    def flow(self) -> int:
        edge = self._gc.edges_data.get(self._v1).get(self._v2)
        return edge.flow

    @flow.setter
    def flow(self, new_flow) -> None:
        edge = self._gc.edges_data.get(self._v1).get(self._v2)
        edge.flow = new_flow

    @property
    def residual_capacity(self) -> int:
        edge = self._gc.edges_data.get(self._v1).get(self._v2)
        return edge.capacity - edge.flow


class FNView(BaseGraph):

    @property
    def source(self) -> FNVertexView | None:
        return self._gc.get_vertex(self._gc.graph_model.source, None)

    @source.setter
    def source(self, new_source: str) -> None:
        self._gc.get_vertex(new_source)
        self._gc.graph_model.source = new_source

    @property
    def sink(self) -> FNVertexView | None:
        return self._gc.get_vertex(self._gc.graph_model.sink, None)

    @sink.setter
    def sink(self, new_sink: str) -> None:
        self._gc.get_vertex(new_sink)
        self._gc.graph_model.sink = new_sink

    def add_edge(self, v1: StrConvertable, v2: StrConvertable) -> FNEdgeView:
        new_edge = self._gc.add_edge(v1, v2)
        return new_edge

    def remove_edge(self, v1: StrConvertable, v2: StrConvertable) -> None:
        self._gc.remove_edge(v1, v2)
        self._gc.remove_edge(v2, v1)
