from .get_floyd_matrix import get_floyd_matrix


def get_eccentricities(graph) -> list[int]:
    '''Нахождение эксцентриситетов'''

    n = len(graph)
    d = get_floyd_matrix(graph)

    e = []

    for row in range(n):
        e.append(max(d[row]))

    return e
