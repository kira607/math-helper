from math_helper.graph.views import EdgeView
from math_helper.graph.views import VertexView


class GraphVertexView(VertexView):

    @property
    def adjacent_vertices(self) -> tuple['GraphVertexView', ...]:
        adjacent_vertices = []
        for ed in self._edges_data[self._name].values():
            if ed:
                adjacent_vertices.append(self._gc.get_vertex(self._name))
        return tuple(adjacent_vertices)

    @property
    def incident_edges(self) -> tuple[EdgeView, ...]:
        incident_edges = []
        for ed in self._edges_data[self._name].values():
            if ed:
                incident_edges.append(ed)
        return tuple(incident_edges)
