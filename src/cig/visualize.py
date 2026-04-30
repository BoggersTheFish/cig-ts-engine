from __future__ import annotations

from pathlib import Path
from math import cos, pi, sin

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

from cig.graph import Graph
from cig.tension import edge_tension


def plot_graph(
    graph: Graph,
    output_path: str | Path,
    highlight_nodes: list[str] | set[str] | None = None,
    title: str | None = None,
) -> None:
    """Render a deterministic circular graph visualization."""
    highlight = set(highlight_nodes or [])
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    positions = _circular_layout(list(graph.nodes))
    edge_tensions = [edge_tension(graph, edge) for edge in graph.edges]
    max_tension = max(edge_tensions, default=0.0)

    figure, axis = plt.subplots(figsize=(14, 14))
    axis.set_aspect("equal")
    axis.axis("off")
    axis.set_title(title or "CIG Graph", fontsize=16, pad=18)

    for edge, tension in zip(graph.edges, edge_tensions, strict=True):
        start = positions[edge.source]
        end = positions[edge.target]
        tension_ratio = tension / max_tension if max_tension > 0.0 else 0.0
        color = _edge_color(tension_ratio)
        width = 0.7 + 3.0 * tension_ratio
        alpha = 0.28 + 0.62 * tension_ratio
        arrow = FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=10 + 8 * tension_ratio,
            linewidth=width,
            color=color,
            alpha=alpha,
            shrinkA=18,
            shrinkB=18,
            connectionstyle="arc3,rad=0.08",
        )
        axis.add_patch(arrow)

    activations = [node.activation for node in graph.nodes.values()]
    max_activation = max(activations, default=1.0) or 1.0
    for node_id, node in graph.nodes.items():
        x, y = positions[node_id]
        activation_ratio = node.activation / max_activation
        size = 280 + 900 * activation_ratio
        node_color = "#f2c94c" if node_id in highlight else _node_color(activation_ratio)
        edge_color = "#111827" if node_id in highlight else "#334155"
        linewidth = 2.4 if node_id in highlight else 1.1
        axis.scatter(
            [x],
            [y],
            s=size,
            c=[node_color],
            edgecolors=edge_color,
            linewidths=linewidth,
            zorder=3,
        )
        axis.text(
            x,
            y - 0.085,
            node.display_label,
            ha="center",
            va="top",
            fontsize=8,
            zorder=4,
        )

    figure.tight_layout()
    figure.savefig(output, dpi=160)
    plt.close(figure)


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


def _circular_layout(node_ids: list[str]) -> dict[str, tuple[float, float]]:
    count = len(node_ids)
    if count == 0:
        return {}
    return {
        node_id: (
            cos(2.0 * pi * index / count + pi / 2.0),
            sin(2.0 * pi * index / count + pi / 2.0),
        )
        for index, node_id in enumerate(node_ids)
    }


def _node_color(activation_ratio: float) -> str:
    inactive = (226, 232, 240)
    active = (37, 99, 235)
    mixed = tuple(
        round(inactive[channel] + (active[channel] - inactive[channel]) * activation_ratio)
        for channel in range(3)
    )
    return "#{:02x}{:02x}{:02x}".format(*mixed)


def _edge_color(tension_ratio: float) -> str:
    relaxed = (100, 116, 139)
    tense = (220, 38, 38)
    mixed = tuple(
        round(relaxed[channel] + (tense[channel] - relaxed[channel]) * tension_ratio)
        for channel in range(3)
    )
    return "#{:02x}{:02x}{:02x}".format(*mixed)
