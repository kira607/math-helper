from math_helper.graph.common import GraphFactory

from .controller import TreeController
from .models import TreeEdgeModel
from .models import TreeModel
from .models import TreeNodeModel
from .views import TreeEdgeView
from .views import TreeNodeView
from .views import TreeView


class TreeFactory(GraphFactory):

    _vertex_model_type = TreeNodeModel
    _vertex_view_type = TreeNodeView
    _edge_model_type = TreeEdgeModel
    _edge_view_type = TreeEdgeView
    _graph_model_type = TreeModel
    _graph_view_type = TreeView
    _controller_type = TreeController
