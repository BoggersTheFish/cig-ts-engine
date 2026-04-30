from cig.edge import Edge
from cig.graph import Graph
from cig.node import Node


def test_context_split_groups_nodes_and_keeps_internal_edges() -> None:
    graph = Graph()
    graph.add_node(Node(id="math_a", context="math"))
    graph.add_node(Node(id="math_b", context="math"))
    graph.add_node(Node(id="culture_a", context="culture"))
    graph.add_edge(Edge(id="internal", source="math_a", target="math_b"))
    graph.add_edge(Edge(id="cross", source="math_a", target="culture_a"))

    contexts = graph.split_by_context()

    assert set(contexts) == {"math", "culture"}
    assert set(contexts["math"].nodes) == {"math_a", "math_b"}
    assert set(contexts["culture"].nodes) == {"culture_a"}
    assert set(contexts["math"].edges) == {"internal"}
