from abc import ABC, abstractmethod
from route_energy.graph.graph import GraphEdge
from route_energy.energy.estimator import EnergyCostEstimator


class CostStrategy(ABC):
    @abstractmethod
    def cost(self, edge: GraphEdge) -> float:
        pass


class DistanceCostStrategy(CostStrategy):
    def cost(self, edge: GraphEdge) -> float:
        return edge.segment.distance_km


class EnergyCostStrategy(CostStrategy):
    def __init__(self, estimator: EnergyCostEstimator):
        self.estimator: EnergyCostEstimator = estimator

    def cost(self, edge: GraphEdge) -> float:
        return self.estimator.estimate(edge.segment)
