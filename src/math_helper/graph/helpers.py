from dot2tex import dot2tex


def get_latex_tikz_string(graph, **kwargs):
    _kwargs = dict(figonly=True, usepdflatex=True, prog='neato', texmode='math', format='tikz')
    _kwargs.update(kwargs)
    tikz = dot2tex(graph.dot(), **_kwargs)
    return f'\\begin{{figure}}[H]\n\\centering\n{tikz}\n\\end{{figure}}'
