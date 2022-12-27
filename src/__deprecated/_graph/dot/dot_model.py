class DotModel:

    def __init__(self):
        self.vertices = {
            'a': {'shape': 'diamond'},
        }
        self._edges = {
            'v1': {
                'v1': {},
                'v2': {'color': 'red'},
            },
            'v2': {
                'v1': {},
                'v2': {},
            },
        }
