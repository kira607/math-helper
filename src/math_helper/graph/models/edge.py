from math_helper.utils import CopyMixin
from math_helper.utils import ReprUtilMixin
from math_helper.utils import Typed
from math_helper.utils.types import StrConvertable


class EdgeModel(ReprUtilMixin, CopyMixin):

    attrs = None

    v1 = Typed(str)
    v2 = Typed(str)

    def __init__(self, v1: StrConvertable, v2: StrConvertable) -> None:
        self.v1 = v1
        self.v2 = v2
        self.attrs = {}

    def __str__(self) -> str:
        _cls = self.__class__.__name__
        return f'{_cls}(v1={self.v1}, v2={self.v2})'

    def __hash__(self) -> int:
        return hash((self.v1, self.v2))

    def __eq__(self, other: 'EdgeModel') -> bool:
        return (self.v1, self.v2) == (other.v1, other.v2)
