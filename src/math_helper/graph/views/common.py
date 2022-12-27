from typing import Any

from math_helper.graph.models import GraphModel
from math_helper.graph.models import VertexModel


class GraphModifier:

    _graph_model: GraphModel = None
    _vertices_data: dict[str, VertexModel] = None
    _edges_data: dict[str, dict[str, Any | None]] = None

    def bind(self, model: GraphModel):  # -> Self
        self._graph_model = model
        self._vertices_data = model.vertices_data
        self._edges_data = model.edges_data
        return self

    @property
    def model(self):
        return self._get_model()

    def _get_model(self):
        raise NotImplementedError()


class UsesController:

    _gc: 'GraphController' = None

    def use_controller(self, controller: 'GraphController'):
        self._gc = controller
