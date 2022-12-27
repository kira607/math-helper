from typing import List, Iterable, Type

from dot2tex import dot2tex

from .digraph import Digraph
from .graph import Graph, Vertex
from .missing import MISSING
from .types import StrConvertable


EdgeTuple = tuple[StrConvertable, StrConvertable]
WeightedEdgeTuple = tuple[StrConvertable, StrConvertable, float]


def mkg(
    vertices: Iterable[StrConvertable] = (),
    edges: Iterable[EdgeTuple | WeightedEdgeTuple] = (),
    label: str = 'G',
    graph_type: Type[Graph] = Graph,
) -> Graph | Digraph:
    graph = graph_type(label=label)
    for vertex in vertices:
        graph.make_vertex(vertex)
    for edge in edges:
        if len(edge) == 2:
            (v1, v2), w = edge, MISSING
        elif len(edge) == 3:
            v1, v2, w = edge
        else:
            raise RuntimeError(f'Invalid edge parameter: {repr(edge)}')
        new_edge = graph.make_edge(v1, v2)
        if w is not MISSING:
            new_edge.weight = w
    return graph


def get_vertices_names(graph: Graph) -> List[str]:
    return [v.name for v in graph.vertices]


def get_latex_tikz_string(graph: Graph):
    return dot2tex(graph.dot, figonly=True, usepdflatex=True, format='tikz')


def make_visited_dict(graph: Graph) -> dict[Vertex, bool]:
    return {vertex: False for vertex in graph}
