from cig.edge import Edge
from cig.graph import CIGraph
from cig.meaning import meaning_derivative
from cig.node import Node
from pytest import approx


def test_meaning_derivative_estimates_activation_sensitivity() -> None:
    graph = CIGraph()
    graph.add_node(Node(id="idea", label="Idea", activation=0.2))
    graph.add_node(Node(id="effect", label="Effect", activation=0.0))
    graph.add_edge(Edge(source="idea", target="effect", relation="supports", weight=0.5))

    derivative = meaning_derivative(graph, input_node_id="idea", perturbation=0.01)

    assert derivative["effect"] == approx(0.5)
