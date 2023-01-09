from math_helper.graph.common.controller_plugins import AdjacencyMatrixPlugin
from math_helper.graph.common.controller_plugins import DotStringPlugin
from math_helper.graph.common.controller_plugins import MergeEdgePlugin
from math_helper.graph.core.controller import GraphController


class NdGraphDotStringPlugin(DotStringPlugin):

    graph = 'digraph'
    arrow = '->'


class NdGraphController(GraphController):
    dot = NdGraphDotStringPlugin()
    merge_edge = MergeEdgePlugin()
    get_adjacency_matrix = AdjacencyMatrixPlugin()
