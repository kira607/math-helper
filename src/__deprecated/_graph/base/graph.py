from typing import Any, Iterator, Type, Callable, Iterable

from math_helper.utils import MISSING
from math_helper.utils.types import StrConvertable

from .graph_data import GraphData
from .edge import Edge, EdgeView
from .vertex import Vertex, VertexView
from .view import GraphElementView


class GraphController:

    _vertex_data_type: Type[Vertex] = Vertex
    _edge_data_type: Type[Edge] = Edge

    def get_vertex(self, vertex_name: StrConvertable, default: Any = MISSING) -> _vertex_view_type | Any:
        vertex_name = str(vertex_name)

        vertex = self._vertices_data.get(vertex_name, default)
        if vertex is MISSING:
            raise KeyError(f'Vertex {vertex_name} is not present in the graph.')
        if vertex is default:
            return default

        view = self._make_vertex_view(vertex_name)
        return view

    def add_vertex(self, vertex_name: StrConvertable) -> _vertex_view_type:
        vertex_name = str(vertex_name)

        existing = self.get_vertex(vertex_name, default=None)
        if existing:
            return existing

        self._vertices_data[vertex_name] = self._make_vertex_data(vertex_name)
        self._edges_data[vertex_name] = {v2.name: None for v2 in self}
        for column in self._edges_data.values():
            column[vertex_name] = None

        view = self._make_vertex_view(vertex_name)
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

    def get_edge(self, v1: StrConvertable, v2: StrConvertable, default: Any = MISSING) -> _edge_view_type:
        v1, v2 = str(v1), str(v2)

        edge = self._edges_data.get(v1, {}).get(v2, default)
        if edge is MISSING:
            raise KeyError(f'Edge {(v1, v2)} is not present in the graph.')
        if edge is default:
            return default

        view = self._make_edge_view(v1, v2)
        return view

    def add_edge(self, v1: StrConvertable, v2: StrConvertable) -> _edge_view_type:
        v1, v2 = str(v1), str(v2)

        existing = self.get_edge(v1, v2, default=None)
        if existing:
            return existing

        self.add_vertex(v1)
        self.add_vertex(v2)
        self._add_edge(v1, v2)

        view = self._make_edge_view(v1, v2)
        return view

    def remove_edge(self, v1: StrConvertable, v2: StrConvertable) -> None:
        v1, v2 = str(v1), str(v2)

        existing = self.get_edge(v1, v2, default=None)
        if not existing:
            return

        self._remove_edge(v1, v2)



class GraphView(GraphElementView):

    _vertex_data_type: Type[Vertex] = Vertex
    _edge_data_type: Type[Edge] = Edge
    _vertex_view_type: Type[VertexView] = VertexView
    _edge_view_type: Type[EdgeView] = EdgeView

    def __len__(self) -> int:
        return len(self._vertices_data)

    def __iter__(self) -> Iterator[_vertex_view_type]:
        return iter(self._make_vertex_view(v) for v in self._vertices_data)

    @property
    def vertices(self) -> tuple[_vertex_view_type]:
        return tuple(self._make_vertex_view(vertex_name) for vertex_name in self._vertices_data)

    @property
    def edges(self) -> tuple[_edge_view_type]:
        visited_edges = set()
        views = []
        for v1 in self._vertices_data:
            for v2 in self._vertices_data:
                edge = self._edges_data[v1][v2]
                if not edge:
                    continue
                if edge in visited_edges:
                    continue
                views.append(self._make_edge_view(v1, v2))
                visited_edges.add(edge)
        return tuple(views)

    def get_vertex(self, vertex_name: StrConvertable, default: Any = MISSING) -> _vertex_view_type | Any:
        vertex_name = str(vertex_name)

        vertex = self._vertices_data.get(vertex_name, default)
        if vertex is MISSING:
            raise KeyError(f'Vertex {vertex_name} is not present in the graph.')
        if vertex is default:
            return default

        view = self._make_vertex_view(vertex_name)
        return view

    def add_vertex(self, vertex_name: StrConvertable) -> _vertex_view_type:
        vertex_name = str(vertex_name)

        existing = self.get_vertex(vertex_name, default=None)
        if existing:
            return existing

        self._vertices_data[vertex_name] = self._make_vertex_data(vertex_name)
        self._edges_data[vertex_name] = {v2.name: None for v2 in self}
        for column in self._edges_data.values():
            column[vertex_name] = None

        view = self._make_vertex_view(vertex_name)
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

    def get_edge(self, v1: StrConvertable, v2: StrConvertable, default: Any = MISSING) -> _edge_view_type:
        v1, v2 = str(v1), str(v2)

        edge = self._edges_data.get(v1, {}).get(v2, default)
        if edge is MISSING:
            raise KeyError(f'Edge {(v1, v2)} is not present in the graph.')
        if edge is default:
            return default

        view = self._make_edge_view(v1, v2)
        return view

    def add_edge(self, v1: StrConvertable, v2: StrConvertable) -> _edge_view_type:
        v1, v2 = str(v1), str(v2)

        existing = self.get_edge(v1, v2, default=None)
        if existing:
            return existing

        self.add_vertex(v1)
        self.add_vertex(v2)
        self._add_edge(v1, v2)

        view = self._make_edge_view(v1, v2)
        return view

    def remove_edge(self, v1: StrConvertable, v2: StrConvertable) -> None:
        v1, v2 = str(v1), str(v2)

        existing = self.get_edge(v1, v2, default=None)
        if not existing:
            return

        self._remove_edge(v1, v2)

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

        merge_edge = merge_edge.get_source_data()
        v1 = self._vertices_data[v1]
        v2 = self._vertices_data[v2]

        for edge in self.edges:
            if edge == merge_edge:
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

    def get_adjacency_matrix(
            self,
            no_path: Any = 0,
            self_cross: Any = 0,
            get_edge_val: Callable[[_edge_data_type], Any] = lambda edge: 1,
    ) -> list[list[Any]]:
        '''
        Get a graph adjacency matrix.

        :param no_path: A value to be put in matrix if there is no edge connecting vertices.
        :param self_cross: A value to be put in matrix for self-crossing vertices (if there is no cycle edge).
        :param get_edge_val: A callable for getting an adjacency matrix cell value if edge connecting vertices exists.
        :return: A graph adjacency matrix
        '''
        n = len(self)
        adjacency_matrix = [
            [
                self_cross if i == j else no_path
                for i in range(n)
            ]
            for j in range(n)
        ]

        for v1, data in self._edges_data.items():
            adjacency_matrix.append([])
            for v2, ed in data.items():

                if ed is None:
                    if v1 == v2:
                        val = self_cross
                    else:
                        val = no_path
                else:
                    val = get_edge_val(ed)

                adjacency_matrix[-1].append(val)

        return adjacency_matrix

    def get_sub_graph(self, vertices: Iterable[StrConvertable]) -> 'Graph':
        sub_graph = self.__class__()

        for v1 in vertices:
            vv = self.get_vertex(v1)
            sub_graph._vertices_data[v1] = vv.get_source_data().copy()
            for v2 in vertices:
                ev = self.get_edge(v1, v2)
                if not sub_graph._edges_data.get(v1):
                    sub_graph._edges_data[v1] = {}
                sub_graph._edges_data[v1][v2] = ev.get_source_data().copy()

        return sub_graph

    def _add_edge(self, v1: str, v2: str) -> None:
        raise NotImplementedError()

    def _remove_edge(self, v1: str, v2: str) -> None:
        raise NotImplementedError()

    def _make_vertex_data(self, name: str) -> _vertex_data_type:
        return self._vertex_data_type(name)

    def _make_edge_data(self, v1: str, v2: str) -> _edge_data_type:
        return self._edge_data_type(v1, v2)

    def _make_vertex_view(self, vertex_name: str) -> _vertex_view_type:
        view = self._vertex_view_type(vertex_name)
        view.link_to_graph(self._graph_data).use_interface(self)
        return view

    def _make_edge_view(self, v1: str, v2: str) -> _edge_view_type:
        view = self._edge_view_type(v1, v2)
        view.link_to_graph(self._graph_data).uses_interface(self)
        return view


class Graph:

    def __new__(cls, *args, **kwargs) -> GraphView:
        data = GraphData()
        view = GraphView()
        view.link_to_graph(data)
        return view
