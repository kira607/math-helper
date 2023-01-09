from typing import Any

from .graph_controller import GraphController
from .graph_modifier import GraphModifier


class ControllerPlugin(GraphModifier):

    def __get__(self, instance: GraphController, owner):
        if instance is None:
            return self

        self.controller = instance
        self.bind(instance.graph_model)

        return self._do()

    def __set_name__(self, owner, name):
        self.public_name = name
        self.protected_name = f'_{name}'

    def __set__(self, instance, value):
        raise AttributeError(f'can\'t set attribute {repr(self.public_name)}')

    def _do(self):
        raise NotImplementedError()

    def copy(self):
        return self.__class__()


class MethodPlugin(ControllerPlugin):

    def _do(self):
        return self.exec

    def exec(self, *args, **kwargs) -> Any:
        raise NotImplementedError()


class PropertyPlugin(ControllerPlugin):

    def _do(self):
        return self.get()

    def get(self) -> Any:
        raise NotImplementedError()
