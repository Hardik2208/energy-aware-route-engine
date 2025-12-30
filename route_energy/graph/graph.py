from typing import Dict, List
from route_energy.domain.segment import RouteSegment


class GraphEdge:
    def __init__(self, from_node: str, to_node: str, segment: RouteSegment):
        self.from_node = from_node
        self.to_node = to_node
        self.segment = segment


class Graph:
    def __init__(self):
        self._adjacency: Dict[str, List[GraphEdge]] = {}

    def add_node(self, node_id: str):
        if node_id not in self._adjacency:
            self._adjacency[node_id] = []

    def add_edge(self, edge: GraphEdge):
        if edge.from_node not in self._adjacency:
            self.add_node(edge.from_node)

        if edge.to_node not in self._adjacency:
            self.add_node(edge.to_node)

        self._adjacency[edge.from_node].append(edge)

    def neighbors(self, node_id: str) -> List[GraphEdge]:
        return self._adjacency.get(node_id, [])

    def nodes(self) -> List[str]:
        return list(self._adjacency.keys())
