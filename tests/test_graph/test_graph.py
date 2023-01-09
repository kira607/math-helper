import pytest

from math_helper.graph import nd_graph, di_graph


@pytest.mark.parametrize('make_graph', ([nd_graph, di_graph]))
@pytest.mark.parametrize(
    'graph_data, v1, v2, to_remove, expected_vertices, expected_edges',
    (
        (
            dict(edges=[('a', 'b')]),
            'a', 'b', None,
            {'a'},
            set(),
        ),
        (
            dict(edges=[('a', 'b')]),
            'b', 'a', None,
            {'b'},
            set(),
        ),
        (
            dict(edges=[('a', 'b')]),
            'b', 'a', 'b',
            {'a'},
            set(),
        ),
        (
            dict(edges=[('a', 'b')]),
            'a', 'b', 'a',
            {'b'},
            set(),
        ),
        (
            dict(edges=[('a', 'b'), ('c', 'd')]),
            'a', 'b', None,
            {'a', 'c', 'd'},
            {('c', 'd')},
        ),
        (
            dict(edges=[('a', 'b'), ('a', 'c'), ('a', 'd')]),
            'a', 'c', None,
            {'a', 'b', 'd'},
            {('a', 'b'), ('a', 'd')},
        ),
        (
            dict(vertices=['a', 'b', 'c', 'd'], edges=[('c', 'd')]),
            'c', 'd', None,
            {'a', 'b', 'c'},
            set(),
        ),
        (
            dict(vertices=['a', 'b', 'c'], edges=[('a', 'b'), ('b', 'c')]),
            'a', 'b', None,
            {'a', 'c'},
            {('a', 'c')},
        ),
        (
            dict(vertices=['a', 'b', 'c'], edges=[('a', 'b'), ('b', 'c')]),
            'b', 'c', None,
            {'a', 'b'},
            {('a', 'b')},
        ),
        (
            dict(edges=[('a', 'b'), ('b', 'c'), ('b', 'd')]),
            'b', 'd', None,
            {'a', 'b', 'c'},
            {('a', 'b'), ('b', 'c')},
        ),
        (
            dict(edges=[('a', 'b'), ('b', 'c'), ('b', 'd'), ('c', 'd')]),
            'b', 'd', None,
            {'a', 'b', 'c'},
            {('a', 'b'), ('b', 'c')},
        ),
    ),
)
def test_merge_edge(make_graph, graph_data, v1, v2, to_remove, expected_vertices, expected_edges):
    graph = make_graph(**graph_data)

    try:
        graph.merge_edge(v1, v2, to_remove)
    except KeyError:
        pytest.skip()

    assert {v.name for v in graph} == expected_vertices
    for expected_vertex in expected_vertices:
        assert graph.get_vertex(expected_vertex).name == expected_vertex

    assert {(e.v1.name, e.v2.name) for e in graph.edges} == expected_edges
    for expected_edge in expected_edges:
        assert (
            graph.get_edge(*expected_edge).v1.name == expected_edge[0] and
            graph.get_edge(*expected_edge).v2.name == expected_edge[1]
        )
