from math_helper.graph.common import GraphFactory

from .controller import FNController
from .models import FNEdgeModel
from .models import FNModel
from .models import FNVertexModel
from .views import FNEdgeView
from .views import FNVertexView
from .views import FNView


class FNFactory(GraphFactory):

    _vertex_model_type = FNVertexModel
    _edge_model_type = FNEdgeModel
    _graph_model_type = FNModel
    _vertex_view_type = FNVertexView
    _edge_view_type = FNEdgeView
    _graph_view_type = FNView
    _controller_type = FNController
