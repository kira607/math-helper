def get_number_of_edges_to_be_full(graph) -> int:
    n = len(graph)
    return int((n * (n - 1)) / 2)


def is_full(graph) -> bool:
    return graph.edges_count == get_number_of_edges_to_be_full(graph)
