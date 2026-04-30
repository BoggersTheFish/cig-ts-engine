from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field

from cig.edge import Edge
from cig.node import Node


@dataclass
class Graph:
    """Mutable deterministic CIG graph state."""

    nodes: dict[str, Node] = field(default_factory=dict)
    edges: dict[str, Edge] = field(default_factory=dict)

    def add_node(self, node: Node) -> None:
        if node.id in self.nodes:
            raise ValueError(f"Duplicate node id: {node.id}")
        self.nodes[node.id] = node

    def add_edge(self, edge: Edge) -> None:
        if edge.id in self.edges:
            raise ValueError(f"Duplicate edge id: {edge.id}")
        if edge.source not in self.nodes:
            raise KeyError(f"Edge source does not exist: {edge.source}")
        if edge.target not in self.nodes:
            raise KeyError(f"Edge target does not exist: {edge.target}")
        self.edges[edge.id] = edge

    def node(self, node_id: str) -> Node:
        return self.nodes[node_id]

    def edge(self, edge_id: str) -> Edge:
        return self.edges[edge_id]

    def outgoing(self, node_id: str) -> list[Edge]:
        return [edge for edge in self.edges.values() if edge.source == node_id]

    def clone(self) -> Graph:
        return deepcopy(self)

    def split_by_context(self) -> dict[str, Graph]:
        """Return subgraphs grouped by node context.

        TODO: Replace this with a proper context-boundary algorithm that can
        preserve selected cross-context constraints.
        """
        grouped: dict[str, Graph] = {}
        for node in self.nodes.values():
            context = node.context or "default"
            grouped.setdefault(context, Graph()).add_node(deepcopy(node))

        for edge in self.edges.values():
            source = self.nodes[edge.source]
            target = self.nodes[edge.target]
            source_context = source.context or "default"
            target_context = target.context or "default"
            if source_context == target_context:
                grouped[source_context].add_edge(deepcopy(edge))

        return grouped

    @classmethod
    def from_records(
        cls,
        nodes: list[dict[str, object]],
        edges: list[dict[str, object]],
    ) -> Graph:
        graph = cls()
        for node_record in nodes:
            graph.add_node(Node(**node_record))
        for edge_record in edges:
            graph.add_edge(Edge(**edge_record))
        return graph

