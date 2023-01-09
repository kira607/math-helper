from typing import Optional, Any

from math_helper.graph.common import EdgeTuple
from math_helper.graph.common.dot_bundle import EdgeViewWithDot
from math_helper.graph.common.dot_bundle import GraphViewWithDot
from math_helper.graph.common.dot_bundle import VertexViewWithDot
from math_helper.utils import MISSING
from math_helper.utils.types import StrConvertable


class TreeNodeView(VertexViewWithDot):

    @property
    def children(self) -> tuple['TreeNodeView', ...]:
        children = []
        for edge in self._gc.pair_matches(self._name, True):
            children.append(edge.v2)
        return tuple(children)

    @property
    def parent(self) -> Optional['TreeNodeView']:
        vm = self._gc.vertices_data[self._name]
        return self._gc.make_vertex_view(vm.parent) if vm.parent else None

    @parent.setter
    def parent(self, new_parent: StrConvertable):
        self._gc.get_vertex(new_parent)
        vm = self._gc.vertices_data[self._name]
        vm._parent = new_parent

    @property
    def gparent(self) -> Optional['TreeNodeView']:
        if self.parent:
            return self.parent.parent
        return None

    def add_child(self, new_child_name: StrConvertable) -> 'TreeNodeView':
        new_edge = self._gc.add_edge(self._name, new_child_name)
        child = new_edge.v2
        child.set_parent(self._name)
        return child

    def remove_child(self, child_name: StrConvertable) -> None:
        self._gc.remove_vertex(child_name)


class TreeEdgeView(EdgeViewWithDot):
    pass


class TreeView(GraphViewWithDot):

    def init_from_edges(self, *edges: EdgeTuple):
        for v1, v2 in edges:
            self._gc.add_mirror_edge(v1, v2)

    @property
    def root(self) -> TreeNodeView | None:
        root = self._gc.graph_model.root
        if root:
            return self._gc.get_vertex(root)
        else:
            return None

    def set_root(self, new_root: StrConvertable):
        new_root = str(new_root)
        if self._gc.get_vertex(new_root, None) is None:
            self._gc.add_vertex(new_root)
        self._gc.graph_model.root = new_root

        # setup nodes parent links
        for parent_name in self._gc.vertices_names:
            for edge in self._gc.pair_matches(parent_name, True):
                child = edge.v2.name
                child = self._gc.vertices_data[child]
                child._parent = parent_name

        return self.root

    def reset_root(self):
        self._gc.graph_model._root = None

        # reset nodes parent links
        for node in self._gc.vertices_data.values():
            node._parent = None

    def get_node(self, name: StrConvertable, default: Any = MISSING) -> TreeNodeView | Any:
        return self._gc.get_vertex(name, default)

    def get_leaves(self) -> list[TreeNodeView]:
        if not self.root:
            raise RuntimeError('Root is not set')

        leaves = []

        for node_name in self._gc.vertices_names:
            incident_edges = tuple(self._gc.pair_matches(node_name, True))
            if len(incident_edges) == 1 and node_name != self._gc.graph_model.root:
                leaves.append(self._gc.make_vertex_view(node_name))

        return leaves
