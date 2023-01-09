from math_helper.utils import ReprUtilMixin
from math_helper.utils.types import StrConvertable

from .uses_controller import UsesController
from .vertex import VertexView


class EdgeView(UsesController, ReprUtilMixin):

    def __init__(self, v1: StrConvertable, v2: StrConvertable) -> None:
        self._v1 = v1
        self._v2 = v2

    def __str__(self) -> str:
        _cls = 'Edge'
        return f'{_cls}(v1={self.v1}, v2={self.v2})'

    def __eq__(self, other: 'EdgeView') -> bool:
        return self._gc.eeq((self._v1, self._v2), (other.v1.name, other.v2.name))

    @property
    def v1(self) -> VertexView:
        return self._gc.make_vertex_view(self._v1)

    @property
    def v2(self) -> VertexView:
        return self._gc.make_vertex_view(self._v2)
