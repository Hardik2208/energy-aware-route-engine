import numpy as np
import pandas as pd

from route_energy.domain.segment import RouteSegment


class EnergyCostEstimator:
    def __init__(self, model):
        self.model = model

        # Validity bounds (from training domain)
        self.DISTANCE_KM_RANGE = (0.5, 10.0)
        self.SPEED_KMPH_RANGE = (20.0, 100.0)
        self.SLOPE_PERCENT_RANGE = (-10.0, 10.0)
        self.TRAFFIC_LEVELS = {0, 1, 2}

    def _clip(self, value, min_val, max_val):
        return max(min(value, max_val), min_val)

    def estimate(self, segment: RouteSegment) -> float:
        # --- Validate & clip ---
        distance = self._clip(
            segment.distance_km,
            *self.DISTANCE_KM_RANGE
        )

        speed = self._clip(
            segment.avg_speed_kmph,
            *self.SPEED_KMPH_RANGE
        )

        slope = self._clip(
            segment.slope_percent,
            *self.SLOPE_PERCENT_RANGE
        )

        traffic = (
            segment.traffic_level
            if segment.traffic_level in self.TRAFFIC_LEVELS
            else max(self.TRAFFIC_LEVELS)
        )

        # --- Feature engineering ---
        speed_squared = speed ** 2
        distance_speed_squared = distance * speed_squared

        # --- Prepare input ---
        row = pd.DataFrame([{
            "distance_km": distance,
            "avg_speed_kmph": speed,
            "slope_percent": slope,
            "traffic_level": traffic,
            "speed_squared": speed_squared,
            "distance_speed_squared": distance_speed_squared
        }])

        # --- Predict ---
        energy = float(self.model.predict(row)[0])

        # --- Enforce non-negativity ---
        return max(energy, 0.0)
