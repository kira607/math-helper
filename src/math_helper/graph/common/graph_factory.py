from math_helper.graph.core.controller import GraphController
from math_helper.graph.core.models import VertexModel, EdgeModel, GraphModel
from math_helper.graph.core.views import VertexView, EdgeView, GraphView


class GraphFactory:

    _vertex_model_type = VertexModel
    _vertex_view_type = VertexView
    _edge_model_type = EdgeModel
    _edge_view_type = EdgeView
    _graph_model_type = GraphModel
    _graph_view_type = GraphView
    _controller_type = GraphController

    def make_vertex_model(self, name: str) -> _vertex_model_type:
        return self._vertex_model_type(name)

    def make_edge_model(self, v1: str, v2: str) -> _edge_model_type:
        return self._edge_model_type(v1, v2)

    def make_graph_model(self) -> _graph_model_type:
        return self._graph_model_type()

    def make_vertex_view(self, vertex_name: str) -> _vertex_view_type:
        return self._vertex_view_type(vertex_name)

    def make_edge_view(self, v1: str, v2: str) -> _edge_view_type:
        return self._edge_view_type(v1, v2)

    def make_graph_view(self) -> _graph_view_type:
        return self._graph_view_type()

    def make_controller(self) -> _controller_type:
        return self._controller_type(self)
