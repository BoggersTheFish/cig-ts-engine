from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from cig.graph import Graph


def plot_activations(graph: Graph, output_path: str | Path | None = None) -> None:
    """Render a simple node activation bar chart.

    TODO: Add graph layout and edge tension visualization.
    """
    labels = [node.display_label for node in graph.nodes.values()]
    activations = [node.activation for node in graph.nodes.values()]

    _, axis = plt.subplots(figsize=(8, 4))
    axis.bar(labels, activations)
    axis.set_ylim(0.0, 1.0)
    axis.set_ylabel("Activation")
    axis.set_title("CIG Node Activations")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()

    if output_path is None:
        plt.show()
    else:
        plt.savefig(output_path)
    plt.close()

