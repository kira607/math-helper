from math_helper.graph.common.dot_bundle import VertexModelWithDot
from math_helper.graph.common.dot_bundle import GraphModelWithDot
from math_helper.graph.common.dot_bundle import EdgeModelWithDot
from math_helper.utils import Typed


class DiGraphVertexModel(VertexModelWithDot):
    pass


class DiGraphEdgeModel(EdgeModelWithDot):

    bidirectional = Typed(bool)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.bidirectional = False

    def __str__(self) -> str:
        _dir = 'both' if self.bidirectional else 'one'
        _cls = self.__class__.__name__
        return f'{_cls}(v1={self.v1}, v2={self.v2}, dir={repr(_dir)})'


class DiGraphModel(GraphModelWithDot):
    pass
