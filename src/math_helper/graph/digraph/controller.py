from math_helper.graph.common.controller_plugins import DotStringPlugin
from math_helper.graph.common.controller_plugins import MergeEdgePlugin, SubGraphPlugin
from math_helper.graph.core.controller import GraphController
from math_helper.graph.core.controller import MethodPlugin


class DiGraphDotStringPlugin(DotStringPlugin):

    graph = 'digraph'
    arrow = '->'


class TransposePlugin(MethodPlugin):

    def exec(self):
        transpose_model = self.controller.graph_model_copy()
        controller = self.controller.copy()
        view = self.controller.graph_elements_factory.make_graph_view()

        controller.bind(transpose_model)
        view.use_controller(controller)

        for edge in controller.edges:
            edge.flip_direction()

        return view


class DiGraphController(GraphController):
    dot = DiGraphDotStringPlugin()
    merge_edge = MergeEdgePlugin()
    get_transpose = TransposePlugin()
    get_sub_graph = SubGraphPlugin()
