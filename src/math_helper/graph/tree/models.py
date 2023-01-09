from typing import Optional

from math_helper.graph.common.dot_bundle import EdgeModelWithDot
from math_helper.graph.common.dot_bundle import GraphModelWithDot
from math_helper.graph.common.dot_bundle import VertexModelWithDot
from math_helper.utils import Typed
from math_helper.utils.types import StrConvertable


class TreeNodeModel(VertexModelWithDot):

    _parent: str | None = None

    @property
    def parent(self) -> str | None:
        return self._parent

    def set_parent(self, parent: str) -> None:
        self._parent = str(parent)


class TreeEdgeModel(EdgeModelWithDot):
    pass


class TreeModel(GraphModelWithDot):

    root = Typed(str, None)

    def __init__(
        self,
        root: Optional[StrConvertable] = None,
        vertices_data=None,
        edges_data=None,
    ) -> None:
        super().__init__(vertices_data, edges_data)
        if root is not None:
            self.root = root
