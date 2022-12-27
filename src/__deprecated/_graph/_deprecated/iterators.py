from enum import Enum
from typing import Optional

from .graph import Graph, Vertex
from .helpers import make_visited_dict


class VertexState(Enum):
    UNVISITED = 1
    PROCESSING = 2
    FINISHED = 3


class GraphIterator:

    def __init__(
        self,
        graph: Graph,
        start_vertex: Optional[Vertex] = None,
        traverse_not_connected: bool = True,
        use_recursive: bool = False,
    ) -> None:
        self._graph = graph

        if not graph:
            to_visit = []
        elif start_vertex is None:
            start_vertex = graph.vertices[0]
            to_visit = [start_vertex]
        else:
            to_visit = [start_vertex]

        self._traverse_not_connected = traverse_not_connected
        self._to_visit = to_visit
        self._visited = make_visited_dict(graph)

    def __next__(self) -> Vertex:
        v = self._get_unvisited_vertex()

        for v2 in self._graph.get_adjacent_vertices(v.name):
            self._add_to_visit(v2)

        return v

    def __iter__(self):
        return self

    def _get_unvisited_vertex(self) -> Vertex:
        visited = True

        while visited:
            if not self._to_visit:
                break
            v = self._to_visit.pop()
            visited = self._visited[v]
            if not visited:
                self._visited[v] = True
                return v

        if all(self._visited.values()):
            raise StopIteration()

        for vertex, visited in self._visited.items():
            if not visited:
                self._visited[vertex] = True
                return vertex

    def _add_to_visit(self, vertex: Vertex) -> None:
        self._to_visit.append(vertex)


class InOrderIterator(GraphIterator):
    '''Dfs iterator going deep and after that returning vertex.'''


class PreOrderIterator(GraphIterator):
    '''Dfs iterator going yielding vertex instantly and then going deeper.'''


class PostOrderIterator(GraphIterator):
    '''Dfs iterator starting from the furthest vertices and going back to start vertex.'''


class DfsIterator(GraphIterator):

    def __next__(self) -> Vertex:
        v = self._get_unvisited_vertex()

        for adjacent_vertex in self._graph.get_adjacent_vertices(v.name):
            self._to_visit.append(adjacent_vertex)

        return v


class BfsIterator(GraphIterator):

    def __next__(self) -> Vertex:
        v = self._get_unvisited_vertex()

        for adjacent_vertex in self._graph.get_adjacent_vertices(v.name):
            self._to_visit.insert(0, adjacent_vertex)

        return v

    def _recursive_traversal(self):
        pass
