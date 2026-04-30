from __future__ import annotations

from pydantic import BaseModel, Field

from cig.graph import Graph


class EdgeTension(BaseModel):
    edge_id: str
    value: float = Field(ge=0.0)


class TensionReport(BaseModel):
    edge_tensions: list[EdgeTension] = Field(default_factory=list)
    total: float = Field(default=0.0, ge=0.0)

    @property
    def coherence(self) -> float:
        """Simple placeholder coherence score in [0, 1]."""
        return 1.0 / (1.0 + self.total)


def edge_tension(graph: Graph, edge_id: str) -> EdgeTension:
    edge = graph.edge(edge_id)
    if edge.expected_target_activation is None:
        return EdgeTension(edge_id=edge.id, value=0.0)

    target_activation = graph.node(edge.target).activation
    value = abs(target_activation - edge.expected_target_activation) * abs(edge.weight)
    return EdgeTension(edge_id=edge.id, value=float(value))


def detect_tension(graph: Graph) -> TensionReport:
    """Detect unresolved constraint error across edges.

    TODO: Generalize tension beyond explicit expected target activation.
    """
    edge_tensions = [edge_tension(graph, edge_id) for edge_id in graph.edges]
    total = sum(item.value for item in edge_tensions)
    return TensionReport(edge_tensions=edge_tensions, total=float(total))

