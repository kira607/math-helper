from math_helper.graph.core.models import VertexModel, EdgeModel, GraphModel
from math_helper.graph.core.views import VertexView, EdgeView, GraphView
from math_helper.utils.types import StrConvertable


class VertexModelWithDot(VertexModel):

    def __init__(self, name: StrConvertable) -> None:
        super().__init__(name)
        self.dot_attrs = {}


class EdgeModelWithDot(EdgeModel):

    def __init__(self, v1: StrConvertable, v2: StrConvertable) -> None:
        super().__init__(v1, v2)
        self.dot_attrs = {}


class GraphModelWithDot(GraphModel):
    def __init__(
        self,
        vertices_data: dict[str, VertexModel] | None = None,
        edges_data: dict[str, dict[str, EdgeModel | None]] | None = None,
    ) -> None:
        super().__init__(vertices_data, edges_data)
        self.graph_attrs = {}
        self.node_attrs = {}
        self.edge_attrs = {}


class VertexViewWithDot(VertexView):

    def set_dot_attrs(self, attrs: dict[str, str]):
        self._gc.vertices_data[self._name].dot_attrs = attrs

    def update_dot_attrs(self, attrs: dict[str, str]):
        self._gc.vertices_data[self._name].dot_attrs.update(attrs)

    def clear_dot_attrs(self):
        self._gc.vertices_data[self._name].dot_attrs = {}


class EdgeViewWithDot(EdgeView):

    def set_dot_attrs(self, attrs: dict[str, str]):
        self._gc.edges_data[self._v1][self._v2].dot_attrs = attrs

    def update_dot_attrs(self, attrs: dict[str, str]):
        self._gc.edges_data[self._v1][self._v2].dot_attrs.update(attrs)

    def clear_dot_attrs(self):
        self._gc.edges_data[self._v1][self._v2].dot_attrs = {}


class GraphViewWithDot(GraphView):

    def dot(self):
        return self._gc.dot()

    def set_graph_attrs(self, attrs: dict[str, str]):
        self._gc.graph_model.graph_attrs = attrs

    def update_graph_attrs(self, attrs: dict[str, str]):
        self._gc.graph_model.graph_attrs.update(attrs)

    def clear_graph_attrs(self):
        self._gc.graph_model.graph_attrs = {}

    def set_edge_attrs(self, attrs: dict[str, str]):
        self._gc.graph_model.edge_attrs = attrs

    def update_edge_attrs(self, attrs: dict[str, str]):
        self._gc.graph_model.edge_attrs.update(attrs)

    def clear_edge_attrs(self):
        self._gc.graph_model.edge_attrs = {}

    def set_node_attrs(self, attrs: dict[str, str]):
        self._gc.graph_model.node_attrs = attrs

    def update_node_attrs(self, attrs: dict[str, str]):
        self._gc.graph_model.node_attrs.update(attrs)

    def clear_node_attrs(self):
        self._gc.graph_model.node_attrs = {}
