from abc import abstractmethod, ABC


DotAttrs = dict[str, str]


class DotController(ABC):

    def __call__(self):
        return self.render()

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


class VertexDot(DotController):

    _attrs: DotAttrs = None

    def __init__(self, vertex):
        self._vertex = vertex
        self._attrs = {}

    def render(self, include_attributes: bool = False) -> str:
        dot_string = f'"{self._vertex.name}"'
        if include_attributes:
            dot_string += self._get_attrs_string(self._attrs, True)
        return dot_string


class EdgeDot(DotController):

    _arrow = '--'
    _attrs: DotAttrs = None

    def __init__(self, edge, vertex_dot_renderer):
        self._edge = edge
        self._attrs = {}

    def render(self, include_attributes: bool = False) -> str:
        arrow = self._arrow
        dot_string = f'{self._edge.v1} {arrow} {self._edge.v2}'
        if include_attributes:
            dot_string += self._get_attrs_string(self._attrs, True)
        return dot_string


class GraphDot(DotController):

    _vertex_attrs: DotAttrs = None
    _edge_attrs: DotAttrs = None
    _graph_attrs: DotAttrs = None

    _type = 'graph'
    _label = 'G'

    _vertex_renderer = VertexDotRenderer
    _edge_renderer = EdgeDotRenderer

    def __init__(self, graph):
        self._graph = graph
        self._vertex_attrs = {}
        self._edge_attrs = {}
        self._graph_attrs = {}
        self._attrs = {}

    def render(self, include_attributes_string: bool = False) -> str:
        start = f'{self._type} {self._label} {{\n'
        vertices_dot = self._get_vertices_dot()
        edges_dot = self._get_edges_dot()
        end = '}'

        dot_string = start + vertices_dot + edges_dot + end
        return dot_string

    def _get_vertices_dot(self) -> str:
        result = ''
        for vertex_view in self._graph.vertices:
            renderer = self._vertex_renderer(vertex_view)
            vertex_dot = renderer.render(include_attributes=True)
            result += '    ' + vertex_dot + '\n'
        return result

    def _get_edges_dot(self) -> str:
        result = ''
        for edge_view in self._graph.edges:
            renderer = self._edge_renderer(edge_view)
            edge_dot = renderer.render(include_attributes=True)
            result += '    ' + edge_dot + '\n'
        return result
