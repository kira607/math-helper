from math_helper.utils.types import StrConvertable

from .common import GraphModifier
from .common import UsesController
from .vertex import VertexView


class EdgeView(GraphModifier, UsesController):

    def __init__(self, v1: StrConvertable, v2: StrConvertable) -> None:
        self._v1 = v1
        self._v2 = v2

    def __str__(self) -> str:
        return str(self._get_model())

    @property
    def v1(self) -> VertexView:
        return self._gc.make_vertex_view(self._v1)

    @property
    def v2(self) -> VertexView:
        return self._gc.make_vertex_view(self._v2)

    @property
    def dot_attrs(self) -> dict:
        return self.model.attrs

    def _get_model(self):
        return self._edges_data[self._v1][self._v2]
