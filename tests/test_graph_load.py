from pathlib import Path

from cig.io import load_graph_yaml


def test_load_graph_from_yaml() -> None:
    graph = load_graph_yaml(Path("examples/ts_core.yaml"))

    assert "forty_seven" in graph.nodes
    assert len(graph.edges) == 3
    assert graph.get_node("forty_seven").activation == 1.0
