from typing import Type, Any, Iterator, Generator

from math_helper.graph.models import EdgeModel
from math_helper.graph.models import GraphModel
from math_helper.graph.models import VertexModel
from math_helper.utils import MISSING
from math_helper.utils.types import StrConvertable

from .common import ModelView
from .edge import EdgeView
from .vertex import VertexView


class GraphController(ModelView):

    def __init__(
        self,
        vertex_model_type: Type[VertexModel] = VertexModel,
        edge_model_type: Type[EdgeModel] = EdgeModel,
        vertex_view_type: Type[VertexView] = VertexView,
        edge_view_type: Type[EdgeView] = EdgeView,
    ):
        self._vertex_model_type = vertex_model_type
        self._edge_model_type = edge_model_type
        self._vertex_view_type = vertex_view_type
        self._edge_view_type = edge_view_type

    # elements generators

    @property
    def vertices(self) -> Generator[VertexView, None, None]:
        for vertex_name in self._vertices_data:
            yield self.make_vertex_view(vertex_name)

    @property
    def edges(self) -> Generator[EdgeView, None, None]:
        visited_edges = set()
        for v1 in self._vertices_data:
            for v2 in self._vertices_data:
                edge = self._edges_data[v1][v2]
                if not edge:
                    continue
                if edge in visited_edges:
                    continue
                visited_edges.add(edge)
                yield self.make_edge_view(v1, v2)

    # basic edges and vertices operations

    def get_vertex(self, vertex_name: StrConvertable, default: Any = MISSING) -> VertexView | Any:
        vertex_name = str(vertex_name)

        vertex = self._vertices_data.get(vertex_name, default)
        if vertex is MISSING:
            raise KeyError(f'Vertex {vertex_name} is not present in the graph.')
        if vertex is default:
            return default

        view = self.make_vertex_view(vertex_name)
        return view

    def add_vertex(self, vertex_name: StrConvertable) -> VertexView:
        vertex_name = str(vertex_name)

        existing = self.get_vertex(vertex_name, default=None)
        if existing:
            return existing

        self._vertices_data[vertex_name] = self.make_vertex_model(vertex_name)
        self._edges_data[vertex_name] = {v2.name: None for v2 in self.vertices}
        for column in self._edges_data.values():
            column[vertex_name] = None

        view = self.make_vertex_view(vertex_name)
        return view

    def remove_vertex(self, vertex_name: StrConvertable) -> None:
        vertex_name = str(vertex_name)

        existing = self.get_vertex(vertex_name, default=None)
        if not existing:
            return

        del self._vertices_data[vertex_name]
        del self._edges_data[vertex_name]
        for column in self._edges_data.values():
            del column[vertex_name]

    def get_edge(self, v1: StrConvertable, v2: StrConvertable, default: Any = MISSING) -> EdgeView:
        v1, v2 = str(v1), str(v2)

        edge = self._edges_data.get(v1, {}).get(v2, default)
        if edge is MISSING:
            raise KeyError(f'Edge {(v1, v2)} is not present in the graph.')
        if edge is default:
            return default

        view = self.make_edge_view(v1, v2)
        return view

    def add_edge(self, v1: StrConvertable, v2: StrConvertable):
        v1, v2 = str(v1), str(v2)

        existing = self.get_edge(v1, v2, default=None)
        if existing:
            return existing

        self.add_vertex(v1)
        self.add_vertex(v2)
        new_edge = self.make_edge_model(v1, v2)
        self.put_edge(new_edge, v1, v2)

        view = self.make_edge_view(v1, v2)
        return view

    def put_edge(self, edge_model: EdgeModel, v1: StrConvertable, v2: StrConvertable) -> None:
        self._edges_data[v1][v2] = edge_model

    def remove_edge(self, v1: StrConvertable, v2: StrConvertable) -> None:
        v1, v2 = str(v1), str(v2)

        existing = self.get_edge(v1, v2, default=None)
        if not existing:
            return

        self._edges_data[v1][v2] = None

    # models and views builders

    def make_vertex_model(self, name: str) -> VertexModel:
        return self._vertex_model_type(name)

    def make_edge_model(self, v1: str, v2: str) -> EdgeModel:
        return self._edge_model_type(v1, v2)

    def make_vertex_view(self, vertex_name: str) -> VertexView:
        view = self._vertex_view_type(vertex_name)
        view.bind(self._graph_model).use_controller(self)
        return view

    def make_edge_view(self, v1: str, v2: str) -> EdgeView:
        view = self._edge_view_type(v1, v2)
        view.bind(self._graph_model).use_controller(self)
        return view

    # abstract methods implementation

    def get_model(self) -> GraphModel:
        return self._graph_model
