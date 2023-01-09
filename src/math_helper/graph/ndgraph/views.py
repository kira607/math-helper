from typing import Any, Callable

from math_helper.graph.common import BaseGraph, GraphVertexView
from math_helper.graph.common.dot_bundle import EdgeViewWithDot
from math_helper.graph.core.models import EdgeModel
from math_helper.utils.types import StrConvertable


class NdGraphVertexView(GraphVertexView):
    pass


class NdGraphEdgeView(EdgeViewWithDot):
    pass


class NdGraphView(BaseGraph):
    '''A base graph model view.'''

    def add_edge(self, v1: StrConvertable, v2: StrConvertable):
        new_edge = self._gc.add_mirror_edge(v1, v2)
        return new_edge

    def remove_edge(self, v1: StrConvertable, v2: StrConvertable) -> None:
        self._gc.remove_edge(v1, v2)
        self._gc.remove_edge(v2, v1)

    def merge_edge(self, v1: StrConvertable, v2: StrConvertable, to_remove: StrConvertable = None):
        self._gc.merge_edge(v1, v2, to_remove)

    def get_adjacency_matrix(
        self,
        no_path: Any = 0,
        self_cross: Any = 0,
        get_edge_val: Callable[['EdgeModel'], Any] = lambda edge_model: 1,
    ) -> list[list[Any]]:
        return self._gc.get_adjacency_matrix(no_path, self_cross, get_edge_val)
