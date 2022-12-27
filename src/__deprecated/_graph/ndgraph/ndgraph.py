import math_helper.graph.base as base


class NdGraph(base.GraphView):

    def _add_edge(self, v1: str, v2: str) -> None:
        new_edge = self._make_edge_data(v1, v2)
        self._edges_data[v1][v2] = new_edge
        self._edges_data[v2][v1] = new_edge

    def _remove_edge(self, v1: str, v2: str) -> None:
        self._edges_data[v1][v2] = None
        self._edges_data[v2][v1] = None
