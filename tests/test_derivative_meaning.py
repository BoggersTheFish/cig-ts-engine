from cig.edge import Edge
from cig.graph import Graph
from cig.meaning import meaning_derivative
from cig.node import Node
from pytest import approx


def test_meaning_derivative_estimates_activation_sensitivity() -> None:
    graph = Graph()
    graph.add_node(Node(id="idea", activation=0.2))
    graph.add_node(Node(id="effect", activation=0.0))
    graph.add_edge(Edge(id="idea_to_effect", source="idea", target="effect", weight=0.5))

    derivative = meaning_derivative(graph, input_node_id="idea", perturbation=0.01)

    assert derivative["effect"] == approx(0.5)
