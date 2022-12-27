from typing import Type

from math_helper.graph.models import EdgeModel
from math_helper.graph.models import GraphModel
from math_helper.graph.models import VertexModel

from .edge import EdgeView
from .graph_controller import GraphController
from .vertex import VertexView


class GraphView:

    _vertex_model_type: Type[VertexModel] = None
    _vertex_view_type: Type[VertexView] = None
    _edge_model_type: Type[EdgeModel] = None
    _edge_view_type: Type[EdgeView] = None

    def __init__(self, graph_model: GraphModel | None = None) -> None:
        self._graph_model = graph_model or GraphModel()
        self._controller = GraphController(
            self._vertex_model_type,
            self._edge_model_type,
            self._vertex_view_type,
            self._edge_view_type,
        )
        self._controller.bind(self._graph_model)

    def __str__(self) -> str:
        return str(self.get_model())

    def __len__(self) -> int:
        return len(self._graph_model.vertices_data)

    def copy(self):
        return self.__class__(self.get_model().copy())

    def get_model(self) -> GraphModel:
        return self._graph_model
