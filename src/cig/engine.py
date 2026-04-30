from __future__ import annotations

import numpy as np

from cig.graph import Graph
from cig.tension import TensionReport, detect_tension


class ThinkingSystemEngine:
    """Deterministic Propagate -> Relax -> Detect Tension -> Evolve loop."""

    def __init__(
        self,
        graph: Graph,
        propagation_rate: float = 1.0,
        relaxation_rate: float = 0.05,
    ) -> None:
        self.graph = graph
        self.propagation_rate = propagation_rate
        self.relaxation_rate = relaxation_rate

    def propagate(self) -> None:
        """Apply one deterministic weighted activation propagation pass.

        TODO: Replace this placeholder with a richer propagation model that
        handles signed constraints, normalization, and attractor search.
        """
        deltas = {node_id: 0.0 for node_id in self.graph.nodes}
        for edge in self.graph.edges:
            source_activation = self.graph.node(edge.source).activation
            deltas[edge.target] += (
                source_activation
                * edge.weight
                * edge.polarity
                * self.propagation_rate
            )

        for node_id, delta in deltas.items():
            node = self.graph.node(node_id)
            node.activation = float(np.clip(node.activation + delta, 0.0, 1.0))

    def relax(self) -> None:
        """Decay activation slightly toward zero.

        TODO: Relaxation should eventually optimize toward low-tension graph
        stability rather than simple activation decay.
        """
        for node in self.graph.nodes.values():
            node.activation = float(np.clip(node.activation * (1.0 - self.relaxation_rate), 0.0, 1.0))

    def detect_tension(self) -> TensionReport:
        return detect_tension(self.graph)

    def evolve(self, report: TensionReport) -> None:
        """Placeholder for Break/Evolve restructuring."""
        # TODO: Split nodes, add constraints, or create new abstractions when
        # unresolved tension justifies added graph complexity.
        _ = report

    def step(self) -> TensionReport:
        self.propagate()
        self.relax()
        report = self.detect_tension()
        self.evolve(report)
        return report
