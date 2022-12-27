from .get_eccentricities import get_eccentricities


def get_radius(graph) -> int:
    eccentricities = get_eccentricities(graph)
    radius = min(eccentricities)
    return radius


def get_diameter(graph) -> int:
    eccentricities = get_eccentricities(graph)
    diameter = max(eccentricities)
    return diameter


def get_centers(graph) -> set[str]:
    eccentricities = get_eccentricities(graph)
    radius = get_radius(graph)
    centers = set()

    for i, e in enumerate(eccentricities):
        if e == radius:
            centers.add(tuple(graph.vertices)[i].name)

    return centers
