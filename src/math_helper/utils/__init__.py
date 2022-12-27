import re
from copy import deepcopy
from typing import Type


class CopyMixin:

    def copy(self):
        return deepcopy(self)


class _Missing:
    def __copy__(self):
        return self

    def __deepcopy__(self):
        return self

    def __repr__(self):
        return f'<{str(self)}>'

    def __str__(self):
        return f'{self.__class__.__name__}'


MISSING = _Missing()


def type_check(instance: object, _type: Type):
    if not isinstance(instance, _type):
        raise TypeError(f'{instance} must be a {_type.__name__} instance.')


class Typed:
    '''
    A descriptor casting value to ``cast_type`` at each ``__set__``.

    Stores data at instance level under protected name.
    '''

    def __init__(self, cast_type: type) -> None:
        self.cast = cast_type

    def __set_name__(self, owner, name):
        self.protected_name = f'_{name}'

    def __set__(self, instance, value):
        instance.__dict__[self.protected_name] = self.cast(value)

    def __get__(self, instance, owner):
        return instance.__dict__[self.protected_name]


def printd(d, indent_step='    ', indent=''):
    for k, v in d.items():
        if isinstance(v, dict):
            print(f'{indent}{k}:')
            printd(v, indent=indent + indent_step)
        else:
            print(f'{indent}{k}: {v}')


class ReprUtilMixin:

    def __repr__(self) -> str:
        return self._default_repr()

    def _default_repr(self) -> str:
        addr = self._get_addr()
        return f'<{str(self)} at {addr}>'

    def _get_addr(self) -> str:
        super_repr = str(super().__repr__())
        matches = re.findall(r'0x[0-9a-f]*', super_repr)
        addr = matches[0]
        return addr
