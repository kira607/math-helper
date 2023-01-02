from typing import Type, Any, Callable

from math_helper.graph.models import EdgeModel
from math_helper.graph.models import GraphModel
from math_helper.graph.models import VertexModel

from .edge import EdgeView
from .graph_controller import GraphController
from .vertex import VertexView


class GraphView:

    _vertex_model_type: Type[VertexModel] = None
    _vertex_view_type: Type[VertexView] = None
    _edge_model_type: Type[EdgeModel] = None
    _edge_view_type: Type[EdgeView] = None

    def __init__(self, graph_model: GraphModel | None = None) -> None:
        self._graph_model = graph_model or GraphModel()
        self._controller = GraphController(
            self._vertex_model_type,
            self._edge_model_type,
            self._vertex_view_type,
            self._edge_view_type,
        )
        self._controller.bind(self._graph_model)

    def __str__(self) -> str:
        return str(self.model)

    def __len__(self) -> int:
        return len(self._graph_model.vertices_data)

    def get_adjacency_matrix(
        self,
        no_path: Any = 0,
        self_cross: Any = 0,
        get_edge_val: Callable[[_edge_model_type], Any] = lambda edge_model: 1,
    ) -> list[list[Any]]:
        '''
        Get a graph adjacency matrix.

        :param no_path: A value to be put in matrix if there is no edge connecting vertices.
        :param self_cross: A value to be put in matrix for self-crossing vertices (if there is no cycle edge).
        :param get_edge_val: A callable for getting an adjacency matrix cell value if edge connecting vertices exists.
        :return: A graph adjacency matrix
        '''
        adjacency_matrix = []

        for v1, data in self._graph_model.edges_data.items():
            adjacency_matrix.append([])
            for v2, ed in data.items():

                if ed is None:
                    if v1 == v2:
                        val = self_cross
                    else:
                        val = no_path
                else:
                    val = get_edge_val(ed)

                adjacency_matrix[-1].append(val)

        return adjacency_matrix

    def copy(self):
        return self.__class__(self.model.copy())

    @property
    def model(self):
        return self._get_model()

    @property
    def graph_attrs(self):
        return self.model.graph_attrs

    @property
    def edge_attrs(self):
        return self.model.edge_attrs

    @property
    def node_attrs(self):
        return self.model.node_attrs

    def _get_model(self) -> GraphModel:
        return self._graph_model
