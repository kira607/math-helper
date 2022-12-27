from typing import Type

from math_helper.graph.common import GraphVertexView
from math_helper.graph.common.base_graph import BaseGraph
from math_helper.graph.models import EdgeModel
from math_helper.graph.models import VertexModel
from math_helper.graph.views import EdgeView
from math_helper.graph.views import VertexView
from math_helper.utils.types import StrConvertable


class NdGraph(BaseGraph):
    '''A base graph model view.'''

    _vertex_model_type: Type[VertexModel] = VertexModel
    _vertex_view_type: Type[VertexView] = GraphVertexView
    _edge_model_type: Type[EdgeModel] = EdgeModel
    _edge_view_type: Type[EdgeView] = EdgeView

    def add_edge(self, v1: StrConvertable, v2: StrConvertable) -> _edge_view_type:
        new_edge = self._controller.add_edge(v1, v2)
        new_edge = new_edge.model
        self._controller.put_edge(new_edge, v2, v1)
        return new_edge

    def remove_edge(self, v1: StrConvertable, v2: StrConvertable) -> None:
        self._controller.remove_edge(v1, v2)
        self._controller.remove_edge(v2, v1)

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

        start = f'graph G {{\n'
        end = '}'
        indent = '    '

        vertices_dot = ''
        for vertex in self.vertices:
            vertex_dot = f'"{vertex.name}"' + _get_attrs_string(vertex.model.attrs)
            vertices_dot += indent + vertex_dot + '\n'

        edges_dot = ''
        for edge in self.edges:
            edge_dot = f'"{edge.v1.name}" -- "{edge.v2.name}"' + _get_attrs_string(edge.model.attrs)
            edges_dot += indent + edge_dot + '\n'

        dot_string = start + vertices_dot + edges_dot + end
        return dot_string

