from math_helper.graph import Tree


def get_prufer_code(tree: Tree) -> list[int]:
    code = []
    while len(code) < len(tree) - 2:
        leafs = tree.get_leaves()
        min_leaf = min(leafs, key=lambda leaf: int(leaf.name))
        parent = min_leaf.parent
        code.append(int(parent.name))
        parent.remove_child(min_leaf.name)

    return code


def graph_from_prufer_code(code: list[int]) -> Tree:
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
