from math_helper.utils import ReprUtilMixin
from math_helper.utils.types import StrConvertable

from .uses_controller import UsesController


class VertexView(UsesController, ReprUtilMixin):
    '''A base vertex view.'''

    def __init__(self, name: StrConvertable) -> None:
        self._name = name

    def __str__(self) -> str:
        _cls = 'Vertex'
        return f'{_cls}({repr(self.name)})'

    def __eq__(self, other: 'VertexView') -> bool:
        return self._gc.veq(self.name, other.name)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: StrConvertable) -> None:
        self._gc.rename_vertex(self.name, new_name)
