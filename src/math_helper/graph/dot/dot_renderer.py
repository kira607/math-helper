from abc import ABC, abstractmethod

import math_helper.graph.base as base


class DotRenderer(ABC):

    _attrs = None

    _element_type: type[base.GraphElementView] = base.GraphElementView

    def __init__(self, element: _element_type, attrs: dict[str, str] = None) -> None:
        self._element = element
        self._attrs = attrs or {}

    @property
    def attrs(self) -> dict[str, str]:
        return self._attrs

    @abstractmethod
    def render(self, include_attributes: bool = False) -> str:
        raise NotImplementedError()

    @staticmethod
    def dict_join(d: dict[str, str]):
        if not d:
            return ''
        joined = ','.join(f'{k}={v}' for k, v in d.items())
        return joined

    def _get_attrs_string(self, add_leading_space: bool = False) -> str:
        joined = self.dict_join(self._attrs)
        if not joined:
            return ''
        leading_space = ' ' if add_leading_space else ''
        return f'{leading_space}[{joined}]'
