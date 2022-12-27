from abc import ABC, abstractmethod
from typing import Dict


class DotAttributesMixin(ABC):

    _dot_attributes = {}
    _default_dot_attributes = {}

    @property
    def dot(self) -> str:
        dot = self.get_dot_string()
        attrs = self._get_dot_attributes_string(True)
        return f'{dot}{attrs}'

    def set_dot_attributes(self, dot_data: Dict[str, str] = None) -> None:
        attrs = self._default_dot_attributes.copy()
        attrs.update(dot_data or {})
        self._dot_attributes = attrs

    def update_dot_attributes(self, dot_data: Dict[str, str]) -> None:
        self._dot_attributes.update(dot_data)

    @abstractmethod
    def get_dot_string(self):
        raise NotImplementedError()
    
    def _get_dot_attributes_string(self, add_leading_space: bool = False):
        if not self._dot_attributes:
            return ''
        attributes = ','.join(f'{k}={v}' for k, v in self._dot_attributes.items())
        leading_space = ' ' if add_leading_space else ''
        return f'{leading_space}[{attributes}]'
