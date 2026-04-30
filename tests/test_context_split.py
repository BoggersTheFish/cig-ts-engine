from cig.edge import Edge
from cig.graph import CIGraph
from cig.node import Node


def test_context_split_groups_nodes_and_keeps_internal_edges() -> None:
    graph = CIGraph()
    graph.add_node(Node(id="math_a", label="Math A", metadata={"context": "math"}))
    graph.add_node(Node(id="math_b", label="Math B", metadata={"context": "math"}))
    graph.add_node(Node(id="culture_a", label="Culture A", metadata={"context": "culture"}))
    graph.add_edge(Edge(source="math_a", target="math_b", relation="related"))
    graph.add_edge(Edge(source="math_a", target="culture_a", relation="related"))

    contexts = graph.split_by_context()

    assert set(contexts) == {"math", "culture"}
    assert set(contexts["math"].nodes) == {"math_a", "math_b"}
    assert set(contexts["culture"].nodes) == {"culture_a"}
    assert len(contexts["math"].edges) == 1
