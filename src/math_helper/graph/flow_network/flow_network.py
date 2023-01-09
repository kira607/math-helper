from typing import Iterable

from math_helper.graph.common import EdgeTuple
from math_helper.utils.types import StrConvertable

from .factory import FNFactory
from .views import FNView


def flow_network(
    vertices: Iterable[StrConvertable] = (),
    edges: Iterable[EdgeTuple] = (),
    source: str | None = None,
    sink: str | None = None,
) -> FNView:
    graph_factory = FNFactory()

    # create
    model = graph_factory.make_graph_model()
    view = graph_factory.make_graph_view()
    controller = graph_factory.make_controller()

    # bind
    controller.bind(model)
    view.use_controller(controller)

    for v in vertices:
        view.add_vertex(v)
    for v1, v2 in edges:
        view.add_edge(v1, v2)
    return view
