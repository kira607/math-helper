from math_helper.utils import Typed, ReprUtilMixin, CopyMixin
from math_helper.utils.types import StrConvertable

from .view import GraphElementView, UsesGraphView


class Edge(ReprUtilMixin, CopyMixin):

    v1 = Typed(str)
    v2 = Typed(str)

    def __init__(self, v1: StrConvertable, v2: StrConvertable) -> None:
        self.v1 = v1
        self.v2 = v2

    def __str__(self) -> str:
        _cls = self.__class__.__name__
        return f'{_cls}(v1={self.v1}, v2={self.v2})'


class EdgeView(GraphElementView, UsesGraphView):

    def __init__(self, v1: StrConvertable, v2: StrConvertable) -> None:
        self._v1 = v1
        self._v2 = v2

    @property
    def v1(self) -> 'VertexView':
        return self._graph.get_vertex(self._v1)

    @property
    def v2(self) -> 'VertexView':
        return self._graph.get_vertex(self._v2)

    def get_source_data(self):
        return self._edges_data[self._v1][self._v2]
