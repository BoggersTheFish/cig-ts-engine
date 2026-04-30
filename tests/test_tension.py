from cig.edge import Edge
from cig.graph import Graph
from cig.node import Node
from cig.tension import detect_tension


def test_tension_uses_expected_target_activation() -> None:
    graph = Graph()
    graph.add_node(Node(id="source", activation=1.0))
    graph.add_node(Node(id="target", activation=0.8))
    graph.add_edge(
        Edge(
            id="constraint",
            source="source",
            target="target",
            relation="constraint",
            weight=1.0,
            expected_target_activation=0.25,
        )
    )

    report = detect_tension(graph)

    assert report.total == 0.55
    assert report.coherence < 1.0

