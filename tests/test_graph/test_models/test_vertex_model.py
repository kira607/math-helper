import pytest

from math_helper.graph.core.models import VertexModel


@pytest.mark.parametrize(
    'v1, v2, expected_eq',
    (
        (VertexModel('a'), VertexModel('a'), True),
        (VertexModel(1), VertexModel(1), True),
        (VertexModel('a'), VertexModel('b'), False),
    ),
)
def test_vertex_model___eq__(v1, v2, expected_eq):
    assert (v1 == v2) == expected_eq
