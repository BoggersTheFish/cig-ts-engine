from cig.edge import Edge
from cig.engine import ThinkingSystemEngine
from cig.graph import CIGraph
from cig.node import Node


def test_propagation_moves_activation_along_weighted_edge() -> None:
    graph = CIGraph()
    graph.add_node(Node(id="source", label="Source", activation=1.0))
    graph.add_node(Node(id="target", label="Target", activation=0.0))
    graph.add_edge(Edge(source="source", target="target", relation="supports", weight=0.5))

    ThinkingSystemEngine(graph, relaxation_rate=0.0).propagate()

    assert graph.get_node("target").activation == 0.5
