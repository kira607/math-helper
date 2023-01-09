from typing import Optional

from math_helper.utils.types import StrConvertable

from .factory import TreeFactory
from .views import TreeView


def tree(root: Optional[StrConvertable] = None) -> TreeView:
    graph_factory = TreeFactory()

    # create
    model = graph_factory.make_graph_model()
    controller = graph_factory.make_controller()
    tree = graph_factory.make_graph_view()

    # bind
    controller.bind(model)
    tree.use_controller(controller)

    if root:
        tree.set_root(root)

    return tree
