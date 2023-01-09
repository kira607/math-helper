from math_helper.graph.common.controller_plugins import DotStringPlugin
from math_helper.graph.core.controller import GraphController


class FNGraphDotStringPlugin(DotStringPlugin):

    graph = 'digraph'
    arrow = '->'


class FNController(GraphController):
    dot = FNGraphDotStringPlugin()
