from typing import List, Iterable, Type

from dot2tex import dot2tex

import math_helper.graph.base as base
from math_helper.utils.types import StrConvertable

from .digraph import DiGraph
from .ndgraph import NdGraph

EdgeTuple = tuple[StrConvertable, StrConvertable]


def _mkg(
    vertices: Iterable[StrConvertable] = (),
    edges: Iterable[EdgeTuple] = (),
    graph_type: Type[NdGraph | DiGraph] = NdGraph,
) -> NdGraph | DiGraph:
    graph = graph_type()
    for vertex in vertices:
        graph.add_vertex(vertex)
    for edge in edges:
        v1, v2 = edge
        graph.add_edge(v1, v2)
    return graph


def mkg(
    vertices: Iterable[StrConvertable] = (),
    edges: Iterable[EdgeTuple] = (),
):
    return _mkg(vertices, edges, NdGraph)


def mkdig(
    vertices: Iterable[StrConvertable] = (),
    edges: Iterable[EdgeTuple] = (),
):
    return _mkg(vertices, edges, DiGraph)


def get_vertices_names(graph: base.Graph) -> List[str]:
    return [v.name for v in graph.vertices]


def make_visited_dict(graph: base.Graph) -> dict[str, bool]:
    return {vertex.name: False for vertex in graph}


def get_latex_tikz_string(graph: NdGraph):
    return dot2tex(graph.dot, figonly=True, usepdflatex=True, format='tikz')
