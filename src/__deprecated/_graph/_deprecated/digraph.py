from .graph import Edge, Vertex
from .graph import Graph
from .types import StrConvertable


class Digraph(Graph):
    '''
    A class representing directional graph.

    Stores graph as a collection of vertices and edges.
    '''

    _dot_name = 'digraph'
    _default_strict_direction: bool = True
    _vertex_type = Vertex
    _edge_type = Edge

    def make_edge(self, v1: StrConvertable, v2: StrConvertable) -> _edge_type:
        edge = super().make_edge(v1, v2)
        edge.directional = True
        return edge

    def get_in_vertices(self, vertex: StrConvertable) -> list[_vertex_type]:
        edges = self.get_in_edges(vertex)
        return [self.get_second(edge, vertex) for edge in edges]

    def get_in_edges(self, vertex: StrConvertable) -> list[_edge_type]:
        vertex = self.get_vertex(vertex)
        out_edges = []
        incident_edges = self.get_incident_edges(vertex.name)

        for incident_edge in incident_edges:
            if incident_edge.v2 == vertex:
                out_edges.append(incident_edge)

        return out_edges

    def in_degree(self, vertex: StrConvertable) -> int:
        in_edges = self.get_in_edges(vertex)
        return len(in_edges)

    def get_out_vertices(self, vertex: StrConvertable) -> list[_vertex_type]:
        edges = self.get_out_edges(vertex)
        return [self.get_second(edge, vertex) for edge in edges]

    def get_out_edges(self, vertex: StrConvertable) -> list[_edge_type]:
        vertex = self.get_vertex(vertex)
        out_edges = []
        incident_edges = self.get_incident_edges(vertex.name)

        for incident_edge in incident_edges:
            if incident_edge.v1 == vertex:
                out_edges.append(incident_edge)

        return out_edges

    def out_degree(self, vertex: StrConvertable) -> int:
        out_edges = self.get_out_edges(vertex)
        return len(out_edges)

    def get_transpose(self) -> 'Digraph':
        transpose = self.copy()
        new_edges = {}

        for key, edge in transpose._edges.items():
            new_edge = edge.copy()
            new_edge.v1, new_edge.v2 = new_edge.v2, new_edge.v1
            new_edges[key[::-1]] = new_edge

        new_vertices = set()
        for edge in new_edges.values():
            new_vertices.add(edge.v1)
            new_vertices.add(edge.v2)

        new_vertices = {v.name: v for v in new_vertices}

        transpose._edges = new_edges
        transpose._edges = new_vertices

        return transpose


