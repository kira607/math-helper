from math_helper.utils.types import StrConvertable

from .common import ModelView
from .common import UsesController
from .vertex import VertexView


class EdgeView(ModelView, UsesController):

    def __init__(self, v1: StrConvertable, v2: StrConvertable) -> None:
        self._v1 = v1
        self._v2 = v2

    def __str__(self) -> str:
        return str(self.get_model())

    @property
    def v1(self) -> VertexView:
        return self._gc.make_vertex_view(self._v1)

    @property
    def v2(self) -> VertexView:
        return self._gc.make_vertex_view(self._v2)

    def get_model(self):
        return self._edges_data[self._v1][self._v2]