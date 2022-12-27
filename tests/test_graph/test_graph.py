import pytest

from math_helper.graph import NdGraph
from math_helper.graph.helpers import nd_graph as mkg
from math_helper.graph.algorithms import is_null, is_full, ChromaticPolynomCreator


@pytest.mark.parametrize(
    'graph, v1, v2, to_remove, expected_vertices, expected_edges',
    (
        (
            mkg(edges=[('a', 'b')]),
            'a', 'b', None,
            {'a'},
            set(),
        ),
        (
            mkg(edges=[('a', 'b')]),
            'b', 'a', None,
            {'b'},
            set(),
        ),
        (
            mkg(edges=[('a', 'b')]),
            'b', 'a', 'b',
            {'a'},
            set(),
        ),
        (
            mkg(edges=[('a', 'b'), ('c', 'd')]),
            'a', 'b', None,
            {'a', 'c', 'd'},
            {('c', 'd')},
        ),
        (
            mkg(edges=[('a', 'b'), ('a', 'c'), ('a', 'd')]),
            'a', 'c', None,
            {'a', 'b', 'd'},
            {('a', 'b'), ('a', 'd')},
        ),
        (
            mkg(['a', 'b', 'c', 'd'], [('c', 'd')]),
            'c', 'd', None,
            {'a', 'b', 'c'},
            set(),
        ),
        (
            mkg(['a', 'b', 'c'], [('a', 'b'), ('b', 'c')]),
            'a', 'b', None,
            {'a', 'c'},
            {('a', 'c')},
        ),
        (
            mkg(['a', 'b', 'c'], [('a', 'b'), ('b', 'c')]),
            'b', 'c', None,
            {'a', 'b'},
            {('a', 'b')},
        ),
        (
            mkg(edges=[('a', 'b'), ('b', 'c'), ('b', 'd')]),
            'b', 'd', None,
            {'a', 'b', 'c'},
            {('a', 'b'), ('b', 'c')},
        ),
        (
            mkg(edges=[('a', 'b'), ('b', 'c'), ('b', 'd'), ('c', 'd')]),
            'b', 'd', None,
            {'a', 'b', 'c'},
            {('a', 'b'), ('b', 'c')},
        ),
    ),
)
def test_merge_edge(graph: NdGraph, v1, v2, to_remove, expected_vertices, expected_edges):
    graph.merge_edge(v1, v2, to_remove)

    assert {v.name for v in graph} == expected_vertices
    for expected_vertex in expected_vertices:
        assert graph.get_vertex(expected_vertex).name == expected_vertex

    assert {(e.v1.name, e.v2.name) for e in graph.edges} == expected_edges
    for expected_edge in expected_edges:
        assert (
            graph.get_edge(*expected_edge).v1.name == expected_edge[0] and
            graph.get_edge(*expected_edge).v2.name == expected_edge[1]
        )
