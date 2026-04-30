from __future__ import annotations

from cig.engine import ThinkingSystemEngine
from cig.graph import Graph


def meaning_derivative(
    graph: Graph,
    input_node_id: str,
    perturbation: float = 0.01,
) -> dict[str, float]:
    """Estimate meaning as d(graph state) / d(input activation).

    This is a finite-difference placeholder over one propagation step.

    TODO: Define richer graph-state observables and multi-step attractor
    derivatives.
    """
    if perturbation <= 0:
        raise ValueError("perturbation must be positive")

    baseline = graph.clone()
    perturbed = graph.clone()

    baseline_engine = ThinkingSystemEngine(baseline, relaxation_rate=0.0)
    perturbed_engine = ThinkingSystemEngine(perturbed, relaxation_rate=0.0)

    input_node = perturbed.node(input_node_id)
    input_node.activation = min(1.0, input_node.activation + perturbation)

    baseline_engine.propagate()
    perturbed_engine.propagate()

    return {
        node_id: (perturbed.node(node_id).activation - baseline.node(node_id).activation) / perturbation
        for node_id in graph.nodes
    }

