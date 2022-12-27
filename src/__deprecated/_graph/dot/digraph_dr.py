import math_helper.graph.dot.base_dr as base
from math_helper.graph.digraph.digraph import DiEdgeView
from math_helper.graph.digraph import DiGraph


class DiGraphVertexDotRenderer(base.VertexDotRenderer):
    pass


class BidirectionalEdgeDotRenderer(base.EdgeDotRenderer):

    _arrow = '->'
    _element_type = DiEdgeView

    def render(self, include_attributes: bool = False) -> str:
        arrow = self._arrow
        dot_string = f'{self._model.v1.name} {arrow} {self._model.v2.name}'
        if self._model.bidirectional:
            self._attrs.update({'dir': 'both'})
        if include_attributes:
            dot_string += self._get_attrs_string(True)
        return dot_string


class DiGraphDotRenderer(base.GraphDotRenderer):

    _type = 'digraph'

    _element_type = DiGraph
    _vertex_renderer = DiGraphVertexDotRenderer
    _edge_renderer = BidirectionalEdgeDotRenderer
