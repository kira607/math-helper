from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import Any, Callable, List, Iterator, Type, Iterable

from math_helper.utils import CopyMixin
from .dot_attributes_mixin import DotAttributesMixin
from .infinity import InfNum
from .missing import MISSING
from .types import StrConvertable
from ..utils import type_check

class Vertex(_BaseVertex):
    '''A base vertex class.'''

class Edge(_BasicEdge):
    '''A base edge class.'''

class DirectionalEdge(_BasicEdge):

    _dot_arrow = '->'
    # _default_dot_attributes = {'dir': 'both'}

    def __hash__(self) -> int:
        return hash(self.v1) - hash(self.v2)


class BidirectionalEdge(_BasicEdge):
    _dot_arrow = '->'
    _default_dot_attributes = {'dir': 'both'}


class Graph(_BaseGraph, CopyMixin):
    '''
    A class representing a non-directional graph.

    Stores graph as a collection of vertices and edges
    '''

    _dot_name: str = 'graph'
    _default_strict_direction: bool = False
    _vertex_type: Type[Vertex] = Vertex
    _edge_type: Type[_BasicEdge] = Edge

    def __init__(self, other: 'Graph' = None, label: str = 'G'):
        self._label = label
        self._vertices = VerticesSet()
        self._edges = EdgesSet(self._vertices)

        if not other:
            return

        for vertex in other.vertices:
            self.add_vertex(vertex)

        for edge in other.edges:
            self.add_edge(edge)

    def __len__(self) -> int:
        return len(self._vertices)

    def __bool__(self) -> bool:
        return bool(len(self))

    def __iter__(self) -> Iterator[_vertex_type]:
        return iter(self._vertices)

    def __repr__(self) -> str:
        cls_name = self.__class__.__name__
        vertices = {v.get_dot_string() for v in self}
        edges = {e.get_dot_string() for e in self.edges}
        return f'<{cls_name} ({vertices}, {edges})>'

    def __contains__(self, item) -> bool:
        if isinstance(item, self._vertex_type):
            return item.name in self._vertices
        if isinstance(item, self._edge_type):
            return item in self._edges._edges
        return False

    @property
    def label(self) -> str:
        return self._label

    @property
    def vertices(self) -> tuple[_vertex_type, ...]:
        return tuple(self._vertices)

    @property
    def edges(self) -> tuple[_edge_type, ...]:
        return tuple(self._edges)

    def get_vertex(self, vertex_name: StrConvertable, default: Any = MISSING) -> _vertex_type:
        '''Get a vertex by name.'''
        return self._vertices.get(vertex_name, default=default)

    def make_vertex(self, name: StrConvertable) -> _vertex_type:
        '''
        Create a vertex and add it to graph.

        If a vertex already exists returns an existing vertex.
        '''
        return self._vertices.make(name)

    def add_vertex(self, vertex: _vertex_type, ok_exists: bool = False) -> _vertex_type:
        '''
        Add and existing vertex to graph.

        Creates a copy of given vertex and adds it to graph.
        A copied vertex is returned.
        '''
        return self._vertices.add(vertex, ok_exists)

    def remove_vertex(self, name: StrConvertable) -> None:
        self._vertices.remove(name)
        # TODO: remove edges linking to this vertex.

    def get_edge(self, v1: StrConvertable, v2: StrConvertable, default: Any = MISSING) -> _edge_type:
        return self._edges.get(v1, v2, default=default)

    def make_edge(self, v1: StrConvertable, v2: StrConvertable) -> _edge_type:
        '''
        Create an edge and add it to graph.

        Creates a new vertices if needed.
        '''
        return self._edges.make(v1, v2)

    def add_edge(self, edge: _edge_type, ok_exists: bool = False) -> _edge_type:
        return self._edges.add(edge, ok_exists)

    def remove_edge(self, v1: StrConvertable, v2: StrConvertable) -> None:
        self._edges.remove(v1, v2)

    def merge_edge(self, v1: str, v2: str) -> None:
        '''
        Merge edge (l, r).

        Removes (l, r) edge and ``r`` vertex.
        All edges connected to ``r`` are reconnected to ``l``.
        '''
        merge_edge = self.get_edge(v1, v2, default=None)
        if not merge_edge:
            return

        v1, v2 = merge_edge.v1, merge_edge.v2

        for edge in self.edges:
            if edge == merge_edge:
                continue
            if edge.v1 == v2:
                edge.v1 = v1
                self.remove_edge(v2.name, edge.v2.name)
                self.make_edge(v1.name, edge.v2.name)
            if edge.v2 == v2:
                self.remove_edge(edge.v1.name, v2.name)
                self.make_edge(edge.v1.name, v1.name)

        self.remove_edge(v1.name, v2.name)
        self.remove_vertex(v2.name)

    def get_adjacency_matrix(
        self,
        no_path: Any,
        self_cross: Any,
        get_edge_val: Callable[[Edge], Any] = lambda edge: 1,
    ) -> List[List[InfNum]]:
        '''
        Get a graph adjacency matrix.

        :param no_path: A value to be put in matrix if there is no edge connecting vertices.
        :param self_cross: A value to be put in matrix for self-crossing vertices (if there is no cycle edge).
        :param get_edge_val: A callable for getting an adjacency matrix cell value if edge connecting vertices exists.

        :return: Target graph adjacency matrix
        '''
        n = len(self)
        adjacency_matrix = [
            [
                self_cross if i == j else no_path
                for i in range(n)
            ]
            for j in range(n)
        ]

        for row, v1 in enumerate(self.vertices):
            for col, v2 in enumerate(self.vertices):
                edge = self.get_edge(v1.name, v2.name, default=None)

                if edge is None:
                    continue

                adjacency_matrix[row][col] = get_edge_val(edge)

        return adjacency_matrix

    def get_incident_edges(self, vertex: StrConvertable) -> list[_edge_type]:
        '''Get edges incident to given vertex.'''
        incident_edges = []
        for v in self:

            e = self.get_edge(vertex, v.name, default=None)

            if e is None:
                continue

            incident_edges.append(e)

        return incident_edges

    def get_adjacent_vertices(self, vertex: StrConvertable) -> List[_vertex_type]:
        '''Get vertices adjacent to the given vertex.'''
        vertex = self.get_vertex(vertex)
        adjacent_vertices = []
        incident_edges = self.get_incident_edges(vertex.name)
        for incident_edge in incident_edges:

            adjacent_vertex = self.get_second(incident_edge, vertex)
            adjacent_vertices.append(adjacent_vertex)

        return adjacent_vertices

    def get_sub_graph(self, vertices: Iterable[StrConvertable]) -> 'Graph':
        sub_graph = self.__class__()
        sub_graph._vertices = {v: self._vertex_type(v) for v in vertices}
        for v1 in vertices:
            for v2 in vertices:
                if self.get_edge(v1, v2, default=None):
                    sub_graph.make_edge(v1, v2)
        return sub_graph

    @staticmethod
    def get_second(edge: _edge_type, first: _vertex_type) -> _vertex_type:
        if edge.v1 == first:
            return edge.v2
        elif edge.v2 == first:
            return edge.v1

    @property
    def dot(self):
        name = self._dot_name
        dot = f'{name} {self.label} {{\n'

        for vertex in self.vertices:
            dot += f'    {vertex.dot}\n'

        for edge in self.edges:
            dot += f'    {edge.dot}\n'
        
        dot += '}'

        return dot
