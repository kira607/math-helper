from math_helper.graph.common.controller_plugins import DotStringPlugin
from math_helper.graph.core.controller import GraphController


class FNGraphDotStringPlugin(DotStringPlugin):

    graph = 'digraph'
    arrow = '->'

    def get_edges_dot(self) -> str:
        edges_dot = ''
        for v1, v2 in self.controller.edges_pairs(True):
            edge = self.edges_data[v1][v2]
            edge_dot_attrs = edge.dot_attrs
            edge_dot = f'"{edge.v1}" {self.arrow} "{edge.v2}"' + self.get_attrs_string(edge_dot_attrs, True)
            edges_dot += self.indent + edge_dot + '\n'

        return edges_dot


class FNController(GraphController):

    dot = FNGraphDotStringPlugin()
