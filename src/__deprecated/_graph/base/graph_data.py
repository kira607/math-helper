from math_helper.utils import CopyMixin


class GraphData(CopyMixin):

    def __init__(self):
        self.edges_data = {}
        self.vertices_data = {}
