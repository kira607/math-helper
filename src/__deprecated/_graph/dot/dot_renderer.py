from abc import ABC, abstractmethod


DotAttrs = dict[str, str]


class DotRenderer(ABC):

    def __init__(self, model) -> None:
        self._model = model

    @abstractmethod
    def render(self, include_attributes: bool = False) -> str:
        raise NotImplementedError()

    @staticmethod
    def dict_join(attrs: DotAttrs):
        if not attrs:
            return ''
        joined = ','.join(f'{k}={v}' for k, v in attrs.items())
        return joined

    def _get_attrs_string(self, attrs: DotAttrs, add_leading_space: bool = False) -> str:
        joined = self.dict_join(attrs)
        if not joined:
            return ''
        leading_space = ' ' if add_leading_space else ''
        return f'{leading_space}[{joined}]'
