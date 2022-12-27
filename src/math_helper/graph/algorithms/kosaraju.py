from math_helper.graph import DiGraph


def make_visited_dict(graph) -> dict[str, bool]:
    return {vertex.name: False for vertex in graph}


class KosarajuAlgorithm:

    @classmethod
    def _fill_stack(cls, graph: DiGraph, vertex, visited, stack):
        visited[vertex] = True

        for out_vertex in graph.get_vertex(vertex.name).out_vertices:
            if not visited[out_vertex]:
                cls._fill_stack(graph, out_vertex, visited, stack)

        stack.append(vertex)

    @classmethod
    def _collect_component(cls, graph, vertex, visited, collected=None):
        visited[vertex] = True

        collected = collected or []

        collected.append(vertex)

        for out_vertex in graph.get_vertex(vertex.name).out_vertices:
            if not visited[out_vertex.name]:
                cls._collect_component(graph, out_vertex, visited, collected)

        return collected

    @classmethod
    def _kosaraju(cls, graph: DiGraph) -> list[list[str]]:

        stack = []
        visited = make_visited_dict(graph)

        for vertex in graph:
            if visited.get(vertex):
                continue
            cls._fill_stack(graph, vertex, visited, stack)

        transpose_graph = graph.get_transpose()
        visited = make_visited_dict(transpose_graph)

        strongly_connected_components_vertices = []
        while stack:
            vertex = stack.pop()
            if visited.get(vertex):
                continue
            component_vertices = [v.name for v in cls._collect_component(transpose_graph, vertex, visited)]
            strongly_connected_components_vertices.append(component_vertices)

        return strongly_connected_components_vertices

    @classmethod
    def get_strongly_connected_components(cls, graph: DiGraph) -> list[DiGraph]:
        strongly_connected_components_vertices = cls._kosaraju(graph)
        strongly_connected_components = []
        for vertices in strongly_connected_components_vertices:
            strongly_connected_component = graph.get_sub_graph(vertices)
            strongly_connected_components.append(strongly_connected_component)
        return strongly_connected_components
