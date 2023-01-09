import re

from copy import deepcopy
from typing import Type, Any


class CopyMixin:
    '''
    A mixin adding copy() method to class.

    Added copy() method returns a deep copy of self.
    '''

    def copy(self):
        '''Get a deep copy of self.'''
        return deepcopy(self)


class _Missing:
    '''A class for explicit designation of missing data.'''

    def __copy__(self):
        return self

    def __deepcopy__(self):
        return self

    def __repr__(self):
        return f'<{str(self)}>'

    def __str__(self):
        return f'{self.__class__.__name__}'


MISSING = _Missing()


def type_check(instance: object, _type: Type) -> None:
    '''
    Check if given ``instance`` is of given ``_type``.

    :param instance: Instance to check.
    :param _type: A type that given instance should have.
    :raises TypeError: Given instance is not of given type.
    :return: None
    '''
    if not isinstance(instance, _type):
        raise TypeError(f'{instance} must be a {_type.__name__} instance.')


class Typed:
    '''
    A descriptor casting value to ``cast_type`` at each ``__set__``.

    Stores data at instance level under protected name.
    '''

    def __init__(self, cast_type: type, default: Any = MISSING) -> None:
        self.cast = cast_type
        self.default = default

    def __set_name__(self, owner, name):
        self.protected_name = f'_{name}'

    def __set__(self, instance, value):
        value = self.cast(value)
        instance.__dict__[self.protected_name] = value

    def __get__(self, instance, owner):
        value = instance.__dict__.get(self.protected_name, self.default)
        if value is MISSING:
            raise AttributeError()
        return value


def printd(d, indent_step='    ', indent=''):
    '''Print dictionary in yaml format.'''
    for k, v in d.items():
        if isinstance(v, dict):
            print(f'{indent}{k}:')
            printd(v, indent_step, indent + indent_step)
        elif isinstance(v, list):
            print(f'{indent}{k}:')
            for i in v:
                print(f'{indent + indent_step}- {i}')
        elif v is None:
            print(f'{indent}{k}: null')
        else:
            print(f'{indent}{k}: {v}')


class ReprUtilMixin:
    '''A mixin adding pretty repr to class.'''

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
