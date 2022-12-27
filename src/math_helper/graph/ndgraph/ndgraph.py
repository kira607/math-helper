from typing import Type

from math_helper.graph.common import GraphVertexView
from math_helper.graph.common.base_graph import BaseGraph
from math_helper.graph.models import EdgeModel
from math_helper.graph.models import VertexModel
from math_helper.graph.views import EdgeView
from math_helper.graph.views import VertexView
from math_helper.utils.types import StrConvertable


class NdGraph(BaseGraph):
    '''A base graph model view.'''

    _vertex_model_type: Type[VertexModel] = VertexModel
    _vertex_view_type: Type[VertexView] = GraphVertexView
    _edge_model_type: Type[EdgeModel] = EdgeModel
    _edge_view_type: Type[EdgeView] = EdgeView

    def add_edge(self, v1: StrConvertable, v2: StrConvertable) -> _edge_view_type:
        new_edge = self._controller.add_edge(v1, v2)
        new_edge = new_edge.get_model()
        self._controller.put_edge(new_edge, v2, v1)
        return new_edge

    def remove_edge(self, v1: StrConvertable, v2: StrConvertable) -> None:
        self._controller.remove_edge(v1, v2)
        self._controller.remove_edge(v2, v1)
