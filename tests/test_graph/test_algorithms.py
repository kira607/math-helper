import pytest

from math_helper.graph import nd_graph as mkg
from math_helper.graph.algorithms import is_null, is_full, ChromaticPolynomCreator


@pytest.mark.parametrize(
    'graph, expected',
    (
        (mkg(['A']), True),
        (mkg(['A', 'B', 'C']), True),
        (mkg(edges=[('A', 'B')]), False),
    ),
)
def test_is_null(graph, expected):
    g = mkg(['A'])
    for e in g.edges:
        print(e)
    graph_is_null = is_null(graph)
    assert graph_is_null == expected


@pytest.mark.parametrize(
    'graph, expected',
    (
        (mkg(['A']), True),
        (mkg(['A', 'B', 'C']), False),
        (mkg(edges=[('A', 'B')]), True),
    ),
)
def test_is_full(graph, expected):
    graph_is_full = is_full(graph)
    assert graph_is_full == expected


@pytest.mark.parametrize(
    'graph, strategy, expected_polynom',
    (
        (mkg(['A']), None, 'K_{1}'),
        (mkg(['A']), 'O', 'O_{1}'),
        (mkg(['A', 'B']), None, 'K_{2} + K_{1}'),
        (mkg(['A', 'B']), 'O', 'O_{2}'),
        (mkg(edges=[('A', 'B')]), None, 'K_{2}'),
        (mkg(edges=[('A', 'B')]), 'O', 'O_{2} + (-1.0) * O_{1}'),
        (
            mkg(edges=[('A', 'B'), ('A', 'D'), ('A', 'C'), ('C', 'D')]),
            'O',
            'O_{4} + (-4.0) * O_{3} + (5.0) * O_{2} + (-2.0) * O_{1}',
        )
    ),
)
def test_get_chromatic_polynom(graph, strategy, expected_polynom) -> None:
    chromatic_polynom = ChromaticPolynomCreator.get_chromatic_polynom(graph, strategy)
    assert chromatic_polynom == expected_polynom
