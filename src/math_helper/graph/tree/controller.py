from math_helper.graph.common.controller_plugins import AdjacencyMatrixPlugin
from math_helper.graph.common.controller_plugins import DotStringPlugin
from math_helper.graph.core.controller import GraphController


class TreeDotStringPlugin(DotStringPlugin):

    graph = 'graph'
    arrow = '--'


class TreeController(GraphController):
    dot = TreeDotStringPlugin()
    get_adjacency_matrix = AdjacencyMatrixPlugin()
