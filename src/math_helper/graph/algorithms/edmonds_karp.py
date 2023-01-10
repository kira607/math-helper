class EdmondsKarpAlgorithm:

    @classmethod
    def get_max_flow(cls, flow_network):
        ap = cls.get_augmenting_path(flow_network)
        while ap:
            bottleneck = min(ap, key=lambda x: x.residual_capacity).residual_capacity
            for edge in ap:
                edge.flow = edge.flow + bottleneck
            ap = cls.get_augmenting_path(flow_network)
        return sum(e.flow for e in flow_network.source.incident_edges)

    @classmethod
    def get_augmenting_path(cls, flow_network):
        queue = [flow_network.source]
        paths = {flow_network.source.name: []}
        while queue:
            u = queue.pop(0)
            for edge in u.out_edges:
                if edge.v2.name in paths or edge.residual_capacity <= 0:
                    continue
                v = edge.v2
                paths[v.name] = paths[u.name] + [edge]
                if v.name == flow_network.sink.name:
                    return paths[v.name]
                queue.append(v)
        return None
