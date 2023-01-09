from math_helper.graph.core.controller import MethodPlugin
from math_helper.utils.types import StrConvertable


class MergeEdgePlugin(MethodPlugin):

    def exec(self, v1: StrConvertable, v2: StrConvertable, to_remove: StrConvertable = None):
        '''
        Merge edge (l, r).

        Removes (l, r) edge and ``r`` vertex.
        All edges connected to ``r`` are reconnected to ``l``.
        '''
        v1, v2 = str(v1), str(v2)

        to_remove = to_remove or v2
        if to_remove not in (v1, v2):
            raise ValueError(f'to_remove must be one of {(v1, v2)}')

        to_leave = v1 if to_remove == v2 else v2

        merge_edge = self.controller.get_edge(v1, v2)

        for edge in self.controller.edges:
            if edge == merge_edge:
                continue

            u = None
            if edge.v1.name == to_remove:
                u = edge.v2.name
            if edge.v2.name == to_remove:
                u = edge.v1.name

            if u:  # (to_remove, u) -> (to_leave, u)
                self.controller.remove_edge(to_remove, u)
                self.controller.add_edge(to_leave, u)

        self.controller.remove_edge(v1, v2)
        self.controller.remove_vertex(to_remove)
