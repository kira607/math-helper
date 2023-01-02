from typing import Type, Optional, Any

from math_helper.graph.models import EdgeModel
from math_helper.graph.models import GraphModel
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
        return self._gc.make_vertex_view(self.model.parent)

    @property
    def gparent(self) -> Optional['TreeNodeView']:
        if self.model.parent:
            return self.model.parent.parent
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

    # TODO: add methods for initialization
    def __init__(self, root: StrConvertable, graph_model: GraphModel | None = None) -> None:
        super().__init__(graph_model)
        self._root = root

    def get_node(self, name: StrConvertable, default: Any = MISSING) -> TreeNodeView | Any:
        return self._controller.get_vertex(name, default)

    def get_leaves(self) -> list[TreeNodeView]:
        leaves = []
        for v1, col in self.model.edges_data.items():
            if sum(1 if v else 0 for v in col.values()) == 1:
                leaves.append(self._controller.make_vertex_view(v1))
        return leaves

    def copy(self):
        return self.__class__(self._root, self.model.copy())

    def dot(self):
        def _dict_join(attrs):
            if not attrs:
                return ''
            joined = ','.join(f'{k}={v}' for k, v in attrs.items())
            return joined

        def _get_attrs_string(attrs, add_leading_space: bool = False) -> str:
            joined = _dict_join(attrs)
            if not joined:
                return ''
            leading_space = ' ' if add_leading_space else ''
            return f'{leading_space}[{joined}]'

        indent = '    '

        start = f'graph G {{\n'
        start += indent + f'graph [{_dict_join(self._graph_model.graph_attrs)}];\n'
        start += indent + f'node [{_dict_join(self._graph_model.node_attrs)}];\n'
        start += indent + f'edge [{_dict_join(self._graph_model.edge_attrs)}];\n'
        end = '}'

        vertices_dot = ''
        for vertex in self._controller.vertices:
            vertex_dot = f'"{vertex.name}"' + _get_attrs_string(vertex.model.attrs)
            vertices_dot += indent + vertex_dot + '\n'

        edges_dot = ''
        for edge in self._controller.edges:
            edge_dot = f'"{edge.v1.name}" -- "{edge.v2.name}"' + _get_attrs_string(edge.model.attrs)
            edges_dot += indent + edge_dot + '\n'

        dot_string = start + vertices_dot + edges_dot + end
        return dot_string
