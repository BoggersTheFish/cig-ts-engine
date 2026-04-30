from cig.edge import Edge
from cig.engine import ThinkingSystemEngine
from cig.graph import Graph
from cig.node import Node


def test_propagation_moves_activation_along_weighted_edge() -> None:
    graph = Graph()
    graph.add_node(Node(id="source", activation=1.0))
    graph.add_node(Node(id="target", activation=0.0))
    graph.add_edge(Edge(id="edge", source="source", target="target", weight=0.5))

    ThinkingSystemEngine(graph, relaxation_rate=0.0).propagate()

    assert graph.node("target").activation == 0.5

