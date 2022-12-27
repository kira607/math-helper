from math_helper.utils.types import StrConvertable

from .common import ModelView
from .common import UsesController


class VertexView(ModelView, UsesController):
    '''A base vertex view.'''

    def __init__(self, name: StrConvertable) -> None:
        self._name = name

    def __str__(self) -> str:
        return str(self.get_model())

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: StrConvertable) -> None:
        if self.name == new_name:
            return

        if new_name in self._vertices_data:
            raise ValueError(
                f'Cannot rename vertex {self.name} -> {new_name}. '
                f'Vertex {new_name} already exists.'
            )

        self._vertices_data[new_name] = self._vertices_data[self.name]

        for vertex_name in self._edges_data:
            self._edges_data[vertex_name][new_name] = self._edges_data[vertex_name][self.name]

        self._edges_data[new_name] = self._edges_data[self.name]
        self._gc.remove_vertex(self.name)

    def get_model(self):
        return self._vertices_data.get(self._name)