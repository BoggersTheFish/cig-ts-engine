from __future__ import annotations

from pydantic import BaseModel, Field

from cig.graph import Graph


class EdgeTension(BaseModel):
    edge_index: int
    source: str
    target: str
    relation: str
    value: float = Field(ge=0.0)


class TensionReport(BaseModel):
    edge_tensions: list[EdgeTension] = Field(default_factory=list)
    total: float = Field(default=0.0, ge=0.0)

    @property
    def coherence(self) -> float:
        """Simple placeholder coherence score in [0, 1]."""
        return 1.0 / (1.0 + self.total)


def edge_tension(graph: Graph, edge_index: int) -> EdgeTension:
    edge = graph.edge(edge_index)
    source_activation = graph.node(edge.source).activation
    target_activation = graph.node(edge.target).activation
    expected = edge.expected_ratio * source_activation * edge.polarity
    value = edge.weight * (target_activation - expected) ** 2
    return EdgeTension(
        edge_index=edge_index,
        source=edge.source,
        target=edge.target,
        relation=edge.relation,
        value=float(value),
    )


def detect_tension(graph: Graph) -> TensionReport:
    """Detect unresolved constraint error across edges.

    Uses tau_ij = weight * (a_j - expected_ratio * polarity * a_i)^2.
    """
    edge_tensions = [edge_tension(graph, edge_index) for edge_index, _ in enumerate(graph.edges)]
    total = sum(item.value for item in edge_tensions)
    return TensionReport(edge_tensions=edge_tensions, total=float(total))
