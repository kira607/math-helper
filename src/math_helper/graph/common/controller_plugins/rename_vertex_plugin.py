from math_helper.graph.core.controller import MethodPlugin


class RenameVertexPlugin(MethodPlugin):

    def exec(self, old_vertex_name: str, new_vertex_name: str):
        if old_vertex_name == new_vertex_name:
            return self.controller.make_vertex_view(old_vertex_name)

        if new_vertex_name in self.controller.vertices_names:
            raise ValueError(
                f'Cannot rename vertex {old_vertex_name} -> {new_vertex_name}. '
                f'Vertex {new_vertex_name} already exists.'
            )

        self.vertices_data[new_vertex_name] = self.vertices_data[old_vertex_name]

        for vertex_name in self.edges_data:
            self.edges_data[vertex_name][new_vertex_name] = self.edges_data[vertex_name][old_vertex_name]

        self.edges_data[new_vertex_name] = self.edges_data[old_vertex_name]
        self.controller.remove_vertex(old_vertex_name)
