from typing import Iterable

from math_helper.graph.common import EdgeTuple
from math_helper.utils.types import StrConvertable

from .factory import NdGraphFactory
from .views import NdGraphView


def nd_graph(
    vertices: Iterable[StrConvertable] = (),
    edges: Iterable[EdgeTuple] = (),
) -> NdGraphView:
    graph_factory = NdGraphFactory()

    # create
    model = graph_factory.make_graph_model()
    controller = graph_factory.make_controller()
    graph = graph_factory.make_graph_view()

    # bind
    controller.bind(model)
    graph.use_controller(controller)

    for v in vertices:
        graph.add_vertex(v)
    for v1, v2 in edges:
        graph.add_edge(v1, v2)
    return graph
