from math_helper.utils import CopyMixin, ReprUtilMixin

from .edge import EdgeModel
from .vertex import VertexModel


class GraphModel(ReprUtilMixin, CopyMixin):

    graph_attrs = None
    node_attrs = None
    edge_attrs = None

    def __init__(
        self,
        vertices_data: dict[str, VertexModel] | None = None,
        edges_data: dict[str, dict[str, EdgeModel | None]] | None = None,
    ) -> None:
        self.edges_data: dict[str, dict[str, EdgeModel | None]] = edges_data or {}
        self.vertices_data: dict[str, VertexModel] = vertices_data or {}
        self.graph_attrs = {}
        self.node_attrs = {}
        self.edge_attrs = {}

    def __str__(self) -> str:
        _cls = self.__class__.__name__
        _vertices = {v.name for v in self.vertices_data.values()}
        _edges = {
            (e.v1, e.v2)
            for v1, col in self.edges_data.items()
            for v2, e in col.items()
            if e
        }
        return f'Graph(V={_vertices}, E={_edges})'

    def __eq__(self, other: 'GraphModel') -> bool:
        # TODO: better graph eq using models comparison
        def edges_key(g):
            return {
                (e.v1, e.v2)
                for v1, col in g.edges_data.items()
                for v2, e in col.items()
                if e
            }

        vertices_same = set(self.vertices_data) == set(other.vertices_data)
        edges_same = edges_key(self) == edges_key(other)
        return vertices_same and edges_same
