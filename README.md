🔌 Energy-Aware Route Comparison Engine for Electric Vehicles
1. Problem Statement

Electric Vehicle (EV) route planning is fundamentally different from traditional navigation.
The shortest-distance route is not always the lowest-energy route due to factors such as:

road slope (gravitational load),
speed-dependent aerodynamic drag,
traffic-induced inefficiencies.

Most routing systems either:
optimize distance or time only, or
apply machine learning end-to-end without correctness guarantees.
This project deliberately separates responsibilities:
Machine Learning is used only to estimate energy consumption.
Classical graph algorithms are used to make routing decisions.
The result is a deterministic, explainable, energy-aware route comparison engine.

2. Design Philosophy

This system is built around four strict principles:
Separation of concerns
ML estimates energy cost
Algorithms decide routes
No logic leakage between layers
Deterministic decision-making
Routing uses Dijkstra’s algorithm
No learning inside routing logic
Interpretable ML
Linear regression with physics-motivated features
No black-box optimization
Explicit assumptions
Synthetic data
Steady-state road segments
No navigation or real-time APIs
The goal is engineering clarity, not feature completeness.

3. System Architecture

High-level execution flow:

Graph (nodes + edges)
        ↓
Dijkstra Router (algorithm-only)
        ↓
Cost Strategy
   ├── Distance cost
   └── Energy cost
           ↓
EnergyCostEstimator (ML model)
        ↓
RouteComparisonService


Key rule:
Routing logic never knows how energy is computed.

4. Energy Estimation Model
4.1 Rule-Based Baseline

A deterministic, physics-inspired baseline model was designed first:
Energy scales linearly with distance
Road slope adds or removes gravitational load
Speed introduces non-linear aerodynamic drag
Traffic acts as an inefficiency multiplier
This baseline serves as controlled ground truth.

4.2 Synthetic Dataset Generation

Due to lack of real EV telemetry:
Realistic feature ranges were sampled
Energy labels were generated using the baseline model

This ensured:

physical consistency
monotonic behavior
controlled experimentation

4.3 ML Approximation

A linear regression model was trained to approximate the baseline.
Initial limitations:
Linear models failed to capture non-linear drag effects

Solution:

Feature engineering using physics-motivated interaction terms:
speed²
distance × speed²

Result:

Interpretable coefficients
Stable behavior
Low error on unseen samples

4.4 Robustness Testing

To validate stability:
Controlled Gaussian noise was injected into energy labels
Coefficient signs and relative importance remained stable
Noise-trained models were used only for analysis, not deployment.

4.5 Model Scope and Limitations

Trained on synthetic data
Assumes steady-state driving per segment
No regenerative braking modeling
No transient acceleration effects
The model is used strictly as a segment-level cost oracle.

5. Routing Engine
5.1 Graph Model

Nodes represent abstract waypoints
Directed edges represent road segments

Each edge carries a RouteSegment:

distance
average speed
slope
traffic level

The graph is:

cost-agnostic
ML-agnostic
algorithm-agnostic

5.2 Dijkstra Routing

Standard Dijkstra implementation

Accepts a cost function:

cost(edge) -> float

Guarantees:

optimality
determinism
correctness (non-negative costs)
No heuristics. No shortcuts.

5.3 Cost Strategies

Two interchangeable cost strategies are implemented:

DistanceCostStrategy
Optimizes total distance
EnergyCostStrategy
Delegates to EnergyCostEstimator
Uses ML-predicted kWh per segment
Switching objectives requires no change to routing logic.

6. Route Comparison Service

The RouteComparisonService orchestrates the system end-to-end:
Accepts a graph and an energy estimator

Computes:

shortest-distance route
lowest-energy route
Returns a structured comparison result

Example output:

{
  'start': 'A',
  'end': 'C',
  'distance_optimal': {
    'cost': 2.0,
    'path': ['A', 'B', 'C']
  },
  'energy_optimal': {
    'cost': 0.315,
    'path': ['A', 'B', 'C']
  }
}


Different graph parameters (slope, speed, traffic) can produce diverging routes without modifying the system.

7. Assumptions & Non-Goals
Explicit Assumptions

Predefined road graph
Segment-level steady-state behavior
Synthetic training data
Explicit Non-Goals
No GPS or navigation
No real-time traffic APIs
No A* or heuristic routing
No end-to-end ML routing

These exclusions are deliberate design decisions, not missing features.

8. Why This Project Matters

This project demonstrates:

Correct use of ML where uncertainty exists
Classical algorithms where correctness matters
Clean architectural boundaries
Engineering discipline over buzzwords

It is intentionally not a product.
It is a systems design exercise.

9. How to Run (Minimal)
pip install -r requirements.txt
python


See RouteComparisonService usage example in the repository.
