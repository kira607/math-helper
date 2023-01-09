from typing import Iterable

from math_helper.graph.core.controller import MethodPlugin
from math_helper.utils.types import StrConvertable


class SubGraphPlugin(MethodPlugin):

    def exec(self, sub_vertices: Iterable[StrConvertable]):
        model = self.controller.graph_model.copy()
        controller = self.controller.copy()
        sub_graph = self.controller.graph_elements_factory.make_graph_view()

        controller.bind(model)
        sub_graph.use_controller(controller)

        sub_vertices = set(sub_vertices)
        this_vertices = set(self.controller.vertices_names)
        diff = this_vertices.difference(sub_vertices)

        for v in diff:
            controller.remove_vertex(v)

        return sub_graph
