from math_helper.graph.common import GraphFactory

from .controller import DiGraphController
from .models import DiGraphEdgeModel
from .models import DiGraphModel
from .models import DiGraphVertexModel
from .views import DiGraphEdgeView
from .views import DiGraphVertexView
from .views import DiGraphView


class DiGraphFactory(GraphFactory):

    _vertex_model_type = DiGraphVertexModel
    _vertex_view_type = DiGraphVertexView
    _edge_model_type = DiGraphEdgeModel
    _edge_view_type = DiGraphEdgeView
    _graph_model_type = DiGraphModel
    _graph_view_type = DiGraphView
    _controller_type = DiGraphController
