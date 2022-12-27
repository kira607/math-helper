from math_helper.infinity import inf


def get_floyd_matrix(graph):
    '''Алгоритм Флойда-Уоршелла'''

    n = len(graph)
    d = graph.get_adjacency_matrix(inf, 0)

    for k in range(n):
        for j in range(n):
            for i in range(n):
                d[i][j] = min(d[i][j], d[i][k] + d[k][j])

    return d
