def find_euler_path(g):
    g = g.copy()
    stack = [next(g.vertices)]
    euler_path = []

    while stack:
        v = stack[-1]
        adj = tuple(v.adjacent_vertices)

        if adj:
            u = adj[0]
            stack.append(u)
            g.remove_edge(v.name, u.name)
        else:
            euler_path.append(stack.pop().name)

    return euler_path