from typing import Type, Optional, Any

from math_helper.graph.models import EdgeModel
from math_helper.graph.models import VertexModel
from math_helper.graph.views import EdgeView
from math_helper.graph.views import GraphView
from math_helper.graph.views import VertexView
from math_helper.utils import MISSING
from math_helper.utils.types import StrConvertable


class TreeNodeModel(VertexModel):

    _parent: str | None = None

    @property
    def parent(self) -> str | None:
        return self._parent

    def set_parent(self, parent: str) -> None:
        self._parent = str(parent)


class TreeNodeView(VertexView):

    @property
    def children(self) -> tuple['TreeNodeView', ...]:
        children = []
        for v2, edge_model in self._edges_data[self._name]:
            if not edge_model:
                continue
            children.append(self._gc.make_vertex_view(v2))
        return tuple(children)

    @property
    def parent(self) -> Optional['TreeNodeView']:
        return self._gc.make_vertex_view(self.get_model().parent)

    @property
    def gparent(self) -> Optional['TreeNodeView']:
        model = self.get_model()
        if model.parent:
            return model.parent.parent
        return None

    def add_child(self, new_child_name: StrConvertable) -> 'TreeNodeView':
        new_edge = self._gc.add_edge(self._name, new_child_name)
        child = new_edge.v2
        child.set_parent(self._name)
        return child

    def remove_child(self, child_name: StrConvertable) -> None:
        self._gc.remove_vertex(child_name)


class Tree(GraphView):
    '''A base graph model view.'''

    _vertex_model_type: Type[VertexModel] = TreeNodeModel
    _vertex_view_type: Type[VertexView] = TreeNodeView
    _edge_model_type: Type[EdgeModel] = EdgeModel
    _edge_view_type: Type[EdgeView] = EdgeView

    _root = None

    # TODO: add methods for initialization

    def get_node(self, name: StrConvertable, default: Any = MISSING) -> TreeNodeView | Any:
        return self._controller.get_vertex(name, default)

    def get_leaves(self) -> list[TreeNodeView]:
        leaves = []
        for v1, col in self.get_model().edges_data.items():
            if not any(col.values()):
                leaves.append(self._controller.make_vertex_view(v1))
        return leaves
