from typing import Callable, Any

from math_helper.graph.core.controller import MethodPlugin
from math_helper.graph.core.models import EdgeModel


class AdjacencyMatrixPlugin(MethodPlugin):

    def exec(
        self,
        no_path: Any = 0,
        self_cross: Any = 0,
        get_edge_val: Callable[[EdgeModel], Any] = lambda edge_model: 1,
    ) -> list[list[Any]]:
        '''
        Get a graph adjacency matrix.

        :param no_path: A value to be put in matrix if there is no edge connecting vertices.
        :param self_cross: A value to be put in matrix for self-crossing vertices (if there is no cycle edge).
        :param get_edge_val: A callable for getting an adjacency matrix cell value if edge connecting vertices exists.
        :return: A graph adjacency matrix
        '''
        adjacency_matrix = []

        for v1 in self.controller.vertices_names:
            adjacency_matrix.append([])
            for v2 in self.controller.vertices_names:
                ed = self.edges_data.get(v1, {}).get(v2, None)

                if ed is None:
                    if v1 == v2:
                        val = self_cross
                    else:
                        val = no_path
                else:
                    val = get_edge_val(ed)

                adjacency_matrix[-1].append(val)

        return adjacency_matrix
