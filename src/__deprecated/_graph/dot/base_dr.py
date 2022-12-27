from math_helper.graph.digraph import DiGraph
from math_helper.graph.ndgraph import NdGraph
from math_helper.graph.views import EdgeView
from math_helper.graph.views import VertexView

from .dot_renderer import DotRenderer


class VertexDotRenderer(DotRenderer):

    _element_type = VertexView

    def render(self, include_attributes: bool = False) -> str:
        dot_string = f'"{self._model.name}"'
        if include_attributes:
            dot_string += self._get_attrs_string(True)
        return dot_string


class EdgeDotRenderer(DotRenderer):

    _arrow = '--'
    _element_type = EdgeView

    def render(self, include_attributes: bool = False) -> str:
        arrow = self._arrow
        dot_string = f'{self._model.v1.name} {arrow} {self._model.v2.name}'
        if include_attributes:
            dot_string += self._get_attrs_string(True)
        return dot_string


class BaseGraphDotRenderer(DotRenderer):

    _type = 'graph'
    _label = 'G'

    _element_type = NdGraph
    _vertex_renderer = VertexDotRenderer
    _edge_renderer = EdgeDotRenderer

    def render(self, include_attributes_string: bool = False) -> str:
        start = f'{self._type} {self._label} {{\n'
        vertices_dot = self._get_vertices_dot()
        edges_dot = self._get_edges_dot()
        end = '}'

        dot_string = start + vertices_dot + edges_dot + end
        return dot_string

    def _get_vertices_dot(self) -> str:
        result = ''
        for vertex_view in self._model:
            renderer = self._vertex_renderer(vertex_view)
            vertex_dot = renderer.render(include_attributes=True)
            result += '    ' + vertex_dot + '\n'
        return result

    def _get_edges_dot(self) -> str:
        result = ''
        for edge_view in self._model.edges:
            renderer = self._edge_renderer(edge_view)
            edge_dot = renderer.render(include_attributes=True)
            result += '    ' + edge_dot + '\n'
        return result


class DiGraphDotRenderer(NdGraphDotRenderer):

    _type = 'digraph'
    _element_type = DiGraph
