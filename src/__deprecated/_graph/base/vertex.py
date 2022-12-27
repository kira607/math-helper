from math_helper.utils import Typed, ReprUtilMixin, CopyMixin
from math_helper.utils.types import StrConvertable

from .view import GraphElementView, UsesGraphView


class Vertex(ReprUtilMixin, CopyMixin):
    '''A base vertex model.'''

    name = Typed(str)

    def __init__(self, name: StrConvertable) -> None:
        self.name = name

    def __str__(self) -> str:
        _cls = self.__class__.__name__
        return f'{_cls}({repr(self.name)})'


class VertexView(GraphElementView, UsesGraphView):
    '''A base vertex view.'''

    def __init__(self, name: StrConvertable) -> None:
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: StrConvertable) -> None:
        if self.name == new_name:
            return

        self._vertices_data[new_name] = self._vertices_data[self.name]

        for vertex_name in self._edges_data:
            self._edges_data[vertex_name][new_name] = self._edges_data[vertex_name][self.name]

        self._edges_data[new_name] = self._edges_data[self.name]
        self._graph.remove_vertex(self.name)

    @property
    def adjacent_vertices(self) -> tuple['VertexView']:
        adjacent_vertices = []
        for ed in self._edges_data[self._name].values():
            if ed:
                adjacent_vertices.append(self._graph.get_vertex(self._name))
        return tuple(adjacent_vertices)

    @property
    def incident_edges(self) -> tuple['EdgeView']:
        incident_edges = []
        for ed in self._edges_data[self._name].values():
            if ed:
                incident_edges.append(ed)
        return tuple(incident_edges)

    def get_source_data(self):
        return self._vertices_data.get(self.name)
