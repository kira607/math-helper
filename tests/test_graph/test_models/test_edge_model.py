import pytest

from math_helper.graph.models import EdgeModel


@pytest.mark.parametrize(
    'v1, v2, expected_eq',
    (
        (EdgeModel('a', 'b'), EdgeModel('a', 'b'), True),
        (EdgeModel(1, 2), EdgeModel('1', '2'), True),
        (EdgeModel('a', 'b'), EdgeModel('a', 'c'), False),
    ),
)
def test_edge_model___eq__(v1, v2, expected_eq):
    assert (v1 == v2) == expected_eq
