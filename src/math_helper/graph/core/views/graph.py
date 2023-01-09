from abc import ABC

from math_helper.utils import ReprUtilMixin, CopyMixin

from .uses_controller import UsesController


class GraphView(UsesController, ReprUtilMixin, CopyMixin, ABC):

    def __str__(self) -> str:
        _cls = 'Graph'
        _vertices = set(self._gc.vertices_names)
        _edges = set(self._gc.edges_pairs(True))
        return f'{_cls}(V={_vertices}, E={_edges})'

    def __len__(self) -> int:
        return self._gc.vertices_count

    def copy(self) -> 'GraphView':
        controller_copy = self._gc.copy()
        model_copy = self._gc.graph_model_copy()
        controller_copy.bind(model_copy)
        view = self.__class__()
        view.use_controller(controller_copy)
        return view
