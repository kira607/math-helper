from math_helper.graph.common import GraphFactory

from .controller import NdGraphController
from .models import NdGraphEdgeModel
from .models import NdGraphModel
from .models import NdGraphVertexModel
from .views import NdGraphEdgeView
from .views import NdGraphVertexView
from .views import NdGraphView


class NdGraphFactory(GraphFactory):

    _vertex_model_type = NdGraphVertexModel
    _edge_model_type = NdGraphEdgeModel
    _graph_model_type = NdGraphModel
    _vertex_view_type = NdGraphVertexView
    _edge_view_type = NdGraphEdgeView
    _graph_view_type = NdGraphView
    _controller_type = NdGraphController
