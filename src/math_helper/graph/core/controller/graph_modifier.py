from typing import Any

from math_helper.graph.core.models import GraphModel
from math_helper.graph.core.models import VertexModel


class GraphModifier:
    '''
    A mixin adding ability to bind view to graph model.

    Children should have a _get_model method.
    '''

    graph_model: GraphModel = None
    vertices_data: dict[str, VertexModel] = None
    edges_data: dict[str, dict[str, Any | None]] = None

    def bind(self, model: GraphModel):  # -> Self
        self.graph_model = model
        self.vertices_data = model.vertices_data
        self.edges_data = model.edges_data
        return self
