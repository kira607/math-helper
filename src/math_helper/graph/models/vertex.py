from math_helper.utils import CopyMixin
from math_helper.utils import ReprUtilMixin
from math_helper.utils import Typed
from math_helper.utils.types import StrConvertable


class VertexModel(ReprUtilMixin, CopyMixin):
    '''A base vertex model.'''

    attrs = None

    name = Typed(str)

    def __init__(self, name: StrConvertable) -> None:
        self.name = name

    def __str__(self) -> str:
        _cls = self.__class__.__name__
        return f'{_cls}({repr(self.name)})'

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other: 'VertexModel') -> bool:
        return self.name == other.name
