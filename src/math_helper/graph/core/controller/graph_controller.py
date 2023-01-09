from typing import Any, Generator, Iterable

from math_helper.graph.core.models import EdgeModel
from math_helper.graph.core.models import GraphModel
from math_helper.graph.core.models import VertexModel
from math_helper.graph.core.views import EdgeView
from math_helper.graph.core.views import VertexView
from math_helper.utils import MISSING
from math_helper.utils.types import StrConvertable

from .graph_modifier import GraphModifier


class GraphController(GraphModifier):

    def __init__(self, graph_elements_factory: 'GraphElementsFactory') -> None:
        self.graph_elements_factory = graph_elements_factory
        self._plugins_registry = {}

    # elements generators and properties

    @property
    def vertices_names(self) -> Generator[str, None, None]:
        for vertex_name in self.vertices_data:
            yield vertex_name

    @property
    def vertices_count(self) -> int:
        return len(self.vertices_data)

    @property
    def vertices(self) -> Generator[VertexView, None, None]:
        for vertex_name in self.vertices_names:
            yield self.make_vertex_view(vertex_name)

    def edges_pairs(self, only_unique: bool = False) -> Generator[tuple[str, str], None, None]:
        visited_edges = set()
        for v1, col in self.edges_data.items():
            for v2, e in col.items():
                if not e:
                    continue
                if e in visited_edges:
                    if only_unique:
                        continue
                    else:
                        yield v1, v2
                else:
                    visited_edges.add(e)
                    yield v1, v2

    @property
    def edges_count(self) -> int:
        return len(tuple(self.edges))

    @property
    def edges(self) -> Generator[EdgeView, None, None]:
        for v1, v2 in self.edges_pairs(True):
            yield self.make_edge_view(v1, v2)

    def pair_matches(self, vertex_name: str, only_existing: bool = False) -> Generator[EdgeView | None, None, None]:
        self.get_vertex(vertex_name)
        for v2 in self.vertices_names:
            nxt = self.edges_data[vertex_name][v2]
            if nxt:
                yield self.make_edge_view(vertex_name, v2)
            elif not only_existing:
                yield nxt

    # general edges and vertices operations

    def get_vertex(self, vertex_name: StrConvertable, default: Any = MISSING) -> VertexView | Any:
        vertex_name = str(vertex_name)

        vertex = self.vertices_data.get(vertex_name, default)
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

        self.vertices_data[vertex_name] = self.make_vertex_model(vertex_name)
        self.edges_data[vertex_name] = {v2: None for v2 in self.vertices_names}
        for column in self.edges_data.values():
            column[vertex_name] = None

        view = self.make_vertex_view(vertex_name)
        return view

    def remove_vertex(self, vertex_name: StrConvertable) -> None:
        vertex_name = str(vertex_name)

        existing = self.get_vertex(vertex_name, default=None)
        if not existing:
            return

        del self.vertices_data[vertex_name]
        del self.edges_data[vertex_name]
        for column in self.edges_data.values():
            del column[vertex_name]

    def get_edge(self, v1: StrConvertable, v2: StrConvertable, default: Any = MISSING) -> EdgeView:
        v1, v2 = str(v1), str(v2)

        edge = self.edges_data.get(v1, {}).get(v2, default)
        if edge is None:
            if default is MISSING:
                raise KeyError(f'Edge {(v1, v2)} is not present in the graph.')
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

    def add_mirror_edge(self, v1: StrConvertable, v2: StrConvertable):
        v1, v2 = str(v1), str(v2)
        self.add_edge(v1, v2)
        added_edge = self.edges_data[v1][v2]
        self.put_edge(added_edge, v2, v1)
        view = self.make_edge_view(v1, v2)
        return view

    def put_edge(self, edge_model: EdgeModel, v1: StrConvertable, v2: StrConvertable) -> None:
        self.edges_data[v1][v2] = edge_model

    def remove_edge(self, v1: StrConvertable, v2: StrConvertable) -> None:
        v1, v2 = str(v1), str(v2)

        existing = self.get_edge(v1, v2, default=None)
        if not existing:
            return

        self.edges_data[v1][v2] = None

    # comparison

    def veq(self, a: StrConvertable, b: StrConvertable):
        a = self.vertices_data.get(a)
        b = self.vertices_data.get(b)
        return a and b and a == b

    def eeq(self, a: tuple[StrConvertable, StrConvertable], b: tuple[StrConvertable, StrConvertable]):
        a = self.edges_data.get(a[0]).get(a[1])
        b = self.edges_data.get(b[0]).get(b[1])
        return a and b and a == b

    # plugins control methods

    def add_plugins(self, plugins: Iterable[tuple[str, 'ControllerPlugin']]):
        for name, plugin in plugins:
            self.add_plugin(name, plugin)

    def add_plugin(self, name: str, plugin: 'ControllerPlugin') -> None:
        if self._plugins_registry.get(name):
            raise ValueError(f'Plugin with name "{name}" already exists.')
        self._plugins_registry[name] = plugin
        setattr(type(self), name, plugin)

    # models and views builders

    def make_vertex_model(self, vertex_name: str) -> VertexModel:
        m = self.graph_elements_factory.make_vertex_model(vertex_name)
        return m

    def make_edge_model(self, v1: str, v2: str) -> EdgeModel:
        m = self.graph_elements_factory.make_edge_model(v1, v2)
        return m

    def make_vertex_view(self, vertex_name: str) -> VertexView:
        view = self.graph_elements_factory.make_vertex_view(vertex_name)
        view.use_controller(self)
        return view

    def make_edge_view(self, v1: str, v2: str) -> EdgeView:
        view = self.graph_elements_factory.make_edge_view(v1, v2)
        view.use_controller(self)
        return view

    # copy

    def copy(self) -> 'GraphController':
        cp = self.__class__(self.graph_elements_factory)
        for name, plugin in self._plugins_registry.items():
            cp.add_plugin(name, plugin.copy())
        return cp

    def graph_model_copy(self) -> GraphModel:
        return self.graph_model.copy()
