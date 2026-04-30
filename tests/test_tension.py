from cig.edge import Edge
from cig.graph import CIGraph
from cig.node import Node
from cig.tension import detect_tension


def test_tension_uses_expected_ratio() -> None:
    graph = CIGraph()
    graph.add_node(Node(id="source", label="Source", activation=1.0))
    graph.add_node(Node(id="target", label="Target", activation=0.8))
    graph.add_edge(
        Edge(
            source="source",
            target="target",
            relation="constraint",
            weight=1.0,
            expected_ratio=0.25,
        )
    )

    report = detect_tension(graph)

    assert report.total == 0.30250000000000005
    assert report.coherence < 1.0
