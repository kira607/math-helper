from typing import Type, Any, Callable, Iterable, Iterator

from math_helper.graph.common import GraphVertexView
from math_helper.graph.models import EdgeModel
from math_helper.graph.models import VertexModel
from math_helper.graph.views import EdgeView
from math_helper.graph.views import GraphView
from math_helper.graph.views import VertexView
from math_helper.utils import MISSING
from math_helper.utils.types import StrConvertable


class BaseGraph(GraphView):
    '''A base graph model view.'''

    _vertex_model_type: Type[VertexModel] = VertexModel
    _vertex_view_type: Type[VertexView] = GraphVertexView
    _edge_model_type: Type[EdgeModel] = EdgeModel
    _edge_view_type: Type[EdgeView] = EdgeView

    def __iter__(self) -> Iterator[_vertex_view_type]:
        return iter(self._controller.vertices)

    @property
    def vertices(self) -> Iterator[_vertex_view_type]:
        return iter(self)

    @property
    def edges(self) -> Iterator[_edge_view_type]:
        return iter(self._controller.edges)

    @property
    def vertices_count(self) -> int:
        return len(tuple(self.vertices))

    @property
    def edges_count(self) -> int:
        return len(tuple(self.edges))

    def get_vertex(self, vertex_name: StrConvertable, default: Any = MISSING) -> _vertex_view_type | Any:
        return self._controller.get_vertex(vertex_name, default)

    def add_vertex(self, vertex_name: StrConvertable) -> _vertex_view_type:
        return self._controller.add_vertex(vertex_name)

    def remove_vertex(self, vertex_name: StrConvertable) -> None:
        self._controller.remove_vertex(vertex_name)

    def get_edge(self, v1: StrConvertable, v2: StrConvertable, default: Any = MISSING) -> _edge_view_type:
        return self._controller.get_edge(v1, v2, default)

    def add_edge(self, v1: StrConvertable, v2: StrConvertable) -> _edge_view_type:
        new_edge = self._controller.add_edge(v1, v2)
        new_edge = new_edge.model
        self._controller.put_edge(new_edge, v2, v1)
        return new_edge

    def remove_edge(self, v1: StrConvertable, v2: StrConvertable) -> None:
        self._controller.remove_edge(v1, v2)
        self._controller.remove_edge(v2, v1)

    def merge_edge(self, v1: StrConvertable, v2: StrConvertable, to_remove: StrConvertable = None) -> None:
        '''
        Merge edge (l, r).

        Removes (l, r) edge and ``r`` vertex.
        All edges connected to ``r`` are reconnected to ``l``.
        '''
        to_remove = to_remove or v2
        if to_remove not in (v1, v2):
            raise ValueError('to_remove must be one of {(v1, v2)}')

        to_leave = v1 if to_remove == v2 else v2

        merge_edge = self.get_edge(v1, v2, default=None)
        if not merge_edge:
            return

        merge_edge = merge_edge._get_model()
        v1 = self._graph_model.vertices_data[v1]
        v2 = self._graph_model.vertices_data[v2]

        for edge in self._controller.edges:
            if edge.model == merge_edge:
                continue

            u = None
            if edge.v1.name == to_remove:
                u = edge.v2.name
            if edge.v2.name == to_remove:
                u = edge.v1.name

            if u:  # (to_remove, u) -> (to_leave, u)
                self.remove_edge(to_remove, u)
                self.add_edge(to_leave, u)

        self.remove_edge(v1.name, v2.name)
        self.remove_vertex(to_remove)

    def get_sub_graph(self, vertices: Iterable[StrConvertable]) -> 'BaseGraph':
        sub_graph = self.__class__()

        for v1 in vertices:
            vv = self.get_vertex(v1)
            sub_graph._graph_model.vertices_data[v1] = vv.get_source_data().copy()
            for v2 in vertices:
                ev = self.get_edge(v1, v2)
                if not sub_graph._graph_model.edges_data.get(v1):
                    sub_graph._graph_model.edges_data[v1] = {}
                sub_graph._graph_model.edges_data[v1][v2] = ev.model.copy()

        return sub_graph
