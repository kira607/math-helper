from math_helper.graph import tree


class PruferSerializer:

    @classmethod
    def serialize(cls, tree) -> list[int]:
        *_, (*_, code) = cls.serialize_by_steps(tree)
        return code

    @classmethod
    def serialize_by_steps(cls, serialize_tree):
        code = []
        code_len = len(serialize_tree) - 2
        while len(code) < code_len:
            leaves = serialize_tree.get_leaves()
            min_leaf = min(leaves, key=lambda leaf: int(leaf.name))
            parent = min_leaf.parent
            code.append(int(parent.name))
            yield serialize_tree, min_leaf, parent, code
            parent.remove_child(min_leaf.name)

    @classmethod
    def deserialize(cls, code):
        *_, last = cls.deserialize_by_steps(code)
        *_, edges = last
        new_tree = tree().init_from_edges(edges)
        return new_tree

    @classmethod
    def deserialize_by_steps(cls, code):
        available_vertices = [i for i in range(1, len(code) + 3)]
        edges = []

        for i, v1 in enumerate(code):
            left_in_code = code[i:]
            not_in_code = [v for v in available_vertices if v not in left_in_code]
            v2 = min(not_in_code)
            new_edge = (str(v1), str(v2))
            edges.append(new_edge)

            yield left_in_code, available_vertices, not_in_code, v2, new_edge, edges

            available_vertices.remove(v2)

        edges.append((str(available_vertices[0]), str(available_vertices[1])))

        yield (
            [],
            available_vertices,
            available_vertices,
            None,
            (str(available_vertices[0]), str(available_vertices[1])),
            edges,
        )


def get_prufer_code(tree) -> list[int]:
    code = []
    while len(code) < len(tree) - 2:
        leafs = tree.get_leaves()
        min_leaf = min(leafs, key=lambda leaf: int(leaf.name))
        parent = min_leaf.parent
        code.append(int(parent.name))
        parent.remove_child(min_leaf.name)

    return code


def graph_from_prufer_code(code: list[int]):
    available_vertices = [i for i in range(1, len(code) + 3)]
    edges = []
    for i, v1 in enumerate(code):
        left_in_code = code[i:]
        not_in_code = [v for v in available_vertices if v not in left_in_code]
        v2 = min(not_in_code)
        available_vertices.remove(v2)
        edges.append((str(v1), str(v2)))
    edges.append((str(available_vertices[0]), str(available_vertices[1])))

    # TODO: put tree initialization after initialization methods
    return None  # mkg(edges=edges)
