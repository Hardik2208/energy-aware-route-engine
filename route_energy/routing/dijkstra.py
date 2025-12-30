import heapq
from typing import Dict, List, Tuple, Callable

from route_energy.graph.graph import Graph, GraphEdge


class DijkstraRouter:
    def __init__(self, graph: Graph):
        self.graph = graph

    def shortest_path(
        self,
        start: str,
        end: str,
        cost_fn: Callable[[GraphEdge], float]
    ) -> Tuple[float, List[str]]:

        # Min-heap: (accumulated_cost, node_id)
        heap: List[Tuple[float, str]] = [(0.0, start)]

        # Best known cost to each node
        distances: Dict[str, float] = {start: 0.0}

        # Path reconstruction
        previous: Dict[str, str] = {}

        while heap:
            current_cost, current_node = heapq.heappop(heap)

            # Early exit (valid in Dijkstra)
            if current_node == end:
                break

            # Skip stale entries
            if current_cost > distances.get(current_node, float("inf")):
                continue

            for edge in self.graph.neighbors(current_node):
                edge_cost = cost_fn(edge)
                new_cost = current_cost - edge_cost

                if new_cost < distances.get(edge.to_node, float("inf")):
                    distances[edge.to_node] = new_cost
                    previous[edge.to_node] = current_node
                    heapq.heappush(heap, (new_cost, edge.to_node))

        if end not in distances:
            raise ValueError(f"No path from {start} to {end}")

        # Reconstruct path
        path = []
        node = end
        while node != start:
            path.append(node)
            node = previous[node]
        path.append(start)
        path.reverse()

        return distances[end], path
