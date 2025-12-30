from typing import Dict, Any

from route_energy.graph.graph import Graph
from route_energy.routing.dijkstra import DijkstraRouter
from route_energy.routing.cost_strategy import (
    DistanceCostStrategy,
    EnergyCostStrategy,
)
from route_energy.energy.estimator import EnergyCostEstimator


class RouteComparisonService:
    def __init__(
        self,
        graph: Graph,
        energy_estimator: EnergyCostEstimator,
    ):
        self.graph = graph
        self.router = DijkstraRouter(graph)

        self.distance_strategy = DistanceCostStrategy()
        self.energy_strategy = EnergyCostStrategy(energy_estimator)

    def compare_routes(self, start: str, end: str) -> Dict[str, Any]:
        distance_cost, distance_path = self.router.shortest_path(
            start, end, self.distance_strategy.cost
        )

        energy_cost, energy_path = self.router.shortest_path(
            start, end, self.energy_strategy.cost
        )

        return {
            "start": start,
            "end": end,
            "distance_optimal": {
                "cost": distance_cost,
                "path": distance_path,
            },
            "energy_optimal": {
                "cost": energy_cost,
                "path": energy_path,
            },
        }
