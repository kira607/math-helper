from math_helper.graph.common.dot_bundle import VertexModelWithDot
from math_helper.graph.common.dot_bundle import GraphModelWithDot
from math_helper.graph.common.dot_bundle import EdgeModelWithDot
from math_helper.utils import Typed


class FNVertexModel(VertexModelWithDot):
    pass


class FNEdgeModel(EdgeModelWithDot):

    capacity = Typed(int)
    flow = Typed(int, 0)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.capacity = 1

    def __str__(self) -> str:
        _cls = self.__class__.__name__
        return f'{_cls}(v1={self.v1}, v2={self.v2}, capacity={self.capacity})'


class FNModel(GraphModelWithDot):

    def __init__(
        self,
        source: str | None = None,
        sink: str | None = None,
        vertices_data=None,
        edges_data=None
    ) -> None:
        super().__init__(vertices_data, edges_data)
        self.source = source
        self.sink = sink
