from math_helper.polynom import Polynom, PolyToken

from .ndgraph import NdGraph


def is_null(graph: NdGraph) -> bool:
    return not bool(len(graph.edges))


def get_number_of_edges_to_be_full(graph: NdGraph) -> int:
    n = len(graph)
    return int((n * (n - 1)) / 2)


def is_full(graph: NdGraph) -> bool:
    return len(graph.edges) == get_number_of_edges_to_be_full(graph)


def get_not_adjacent_vertices(graph: NdGraph) -> list[tuple[str, str]]:
    not_adjacent_vertices = []
    for v1 in graph:
        for v2 in graph:
            if graph.get_edge(v1.name, v2.name, default=None):
                continue
            if v1 == v2:
                continue
            not_adjacent_vertices.append((v1.name, v2.name))
    return not_adjacent_vertices


class ChromaticPolynomCreator:
    '''A chromatic polynom creator for non-directional graph.'''

    @classmethod
    def pick_optimal_strategy(cls, graph: NdGraph):
        n = len(graph)
        if get_number_of_edges_to_be_full(graph) / 2 > n:
            strategy = 'O'
        else:
            strategy = 'K'
        return strategy

    @classmethod
    def get_chromatic_polynom(cls, graph: NdGraph, strategy=None) -> str:
        poly = cls._get_chromatic_polynom(graph, strategy)
        return str(poly)

    @classmethod
    def _get_chromatic_polynom(cls, graph: NdGraph, strategy=None) -> Polynom:
        n = len(graph)
        strategy = strategy or cls.pick_optimal_strategy(graph)

        if strategy == 'O':
            if is_null(graph):
                return Polynom.from_tokens(PolyToken(f'O_{{{n}}}'))
            return cls.o_strategy(graph)

        if strategy == 'K':
            if is_full(graph):
                return Polynom.from_tokens(PolyToken(f'K_{{{n}}}'))
            return cls.k_strategy(graph)

    @classmethod
    def o_strategy(cls, graph: NdGraph) -> Polynom:
        '''to O : P(G_1, x) = P(G, x) - P(G_2, x)'''
        next_strategy = 'O'

        g = graph.copy()
        target_edge = g.edges[0].v1.name, g.edges[0].v2.name
        g.remove_edge(*target_edge)
        g2 = graph.copy()
        g2.merge_edge(*target_edge)

        left = cls._get_chromatic_polynom(g, next_strategy)
        right = cls._get_chromatic_polynom(g2, next_strategy)
        return left - right

    @classmethod
    def k_strategy(cls, graph: NdGraph) -> Polynom:
        '''to K : P(G, x) = P(G_1, x) + P(G_2, x)'''
        next_strategy = 'K'

        v1, v2 = get_not_adjacent_vertices(graph)[0]
        g1 = graph.copy()
        g1.add_edge(v1, v2)
        g2 = g1.copy()
        g2.merge_edge(v1, v2)

        left = cls._get_chromatic_polynom(g1, next_strategy)
        right = cls._get_chromatic_polynom(g2, next_strategy)
        return left + right
