import pytest

from math_helper.graph.core.models import EdgeModel, GraphModel, VertexModel


@pytest.mark.parametrize(
    'v1, v2, expected_eq',
    (
        (
            GraphModel(
                {
                    'a': VertexModel('a'),
                    'b': VertexModel('b'),
                    'c': VertexModel('c'),
                    'd': VertexModel('d'),
                },
                {
                    'a': {'a': None, 'b': EdgeModel('a', 'b'), 'c': None, 'd': None},
                    'b': {'a': None, 'b': None, 'c': None, 'd': None},
                    'c': {'a': None, 'b': None, 'c': None, 'd': None},
                    'd': {'a': None, 'b': None, 'c': None, 'd': None},
                },
            ),
            GraphModel(
                {
                    'a': VertexModel('a'),
                    'b': VertexModel('b'),
                    'c': VertexModel('c'),
                    'd': VertexModel('d'),
                },
                {
                    'a': {'a': None, 'b': EdgeModel('a', 'b'), 'c': None, 'd': None},
                    'b': {'a': None, 'b': None, 'c': None, 'd': None},
                    'c': {'a': None, 'b': None, 'c': None, 'd': None},
                    'd': {'a': None, 'b': None, 'c': None, 'd': None},
                },
            ),
            True
        ),
    ),
)
def test_graph_model___eq__(v1, v2, expected_eq):
    assert (v1 == v2) == expected_eq
