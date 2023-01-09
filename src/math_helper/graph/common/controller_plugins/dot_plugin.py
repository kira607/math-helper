from abc import ABC
from typing import Any

from math_helper.graph.core.controller import PropertyPlugin


class DotStringPlugin(PropertyPlugin, ABC):

    indent = '    '
    graph = None
    arrow = None
    label = 'G'

    def __call__(self):
        start = self.get_start()
        global_attrs = self.get_global_attrs()
        vertices_dot = self.get_vertices_dot()
        edges_dot = self.get_edges_dot()
        end = '}'

        dot_string = start + global_attrs + vertices_dot + edges_dot + end

        return dot_string

    def get(self) -> Any:
        return self

    def get_start(self) -> str:
        start = f'{self.graph} {self.label} {{\n'
        return start

    def get_global_attrs(self) -> str:
        global_attrs = ''

        graph_attrs = self.dict_join(self.graph_model.graph_attrs)
        if graph_attrs:
            global_attrs += self.indent + f'graph [{graph_attrs}];\n'

        node_attrs = self.dict_join(self.graph_model.node_attrs)
        if node_attrs:
            global_attrs += self.indent + f'node [{node_attrs}];\n'

        edge_attrs = self.dict_join(self.graph_model.edge_attrs)
        if edge_attrs:
            global_attrs += self.indent + f'edge [{edge_attrs}];\n'

        return global_attrs

    def get_vertices_dot(self) -> str:
        vertices_dot = ''
        for vertex in self.vertices_data.values():
            vertex_dot_attrs = vertex.dot_attrs
            vertex_dot = f'"{vertex.name}"' + self.get_attrs_string(vertex_dot_attrs, True)
            vertices_dot += self.indent + vertex_dot + '\n'

        return vertices_dot

    def get_edges_dot(self) -> str:
        edges_dot = ''
        for v1, v2 in self.controller.edges_pairs(True):
            edge = self.edges_data[v1][v2]
            edge_dot_attrs = edge.dot_attrs
            edge_dot = f'"{edge.v1}" {self.arrow} "{edge.v2}"' + self.get_attrs_string(edge_dot_attrs, True)
            edges_dot += self.indent + edge_dot + '\n'

        return edges_dot

    @classmethod
    def dict_join(cls, attrs):
        if not attrs:
            return ''
        joined = ','.join(f'{k}={v}' for k, v in attrs.items())
        return joined

    @classmethod
    def get_attrs_string(cls, attrs, add_leading_space: bool = False) -> str:
        joined = cls.dict_join(attrs)
        if not joined:
            return ''
        leading_space = ' ' if add_leading_space else ''
        return f'{leading_space}[{joined}]'
