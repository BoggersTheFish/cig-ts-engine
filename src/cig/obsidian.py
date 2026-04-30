from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from cig.edge import Edge
from cig.graph import Graph
from cig.node import Node
from cig.tension import edge_tension, total_tension


def export_obsidian(graph: Graph, output_dir: str | Path) -> Path:
    """Export a CIG graph as an Obsidian-compatible Markdown vault."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    edge_rows = _edge_rows(graph)
    for node_id, node in graph.nodes.items():
        (output_path / f"{node_id}.md").write_text(
            _render_node_note(graph, node, edge_rows),
            encoding="utf-8",
        )

    (output_path / "index.md").write_text(
        _render_index(graph),
        encoding="utf-8",
    )
    (output_path / "edges.md").write_text(
        _render_edges(edge_rows),
        encoding="utf-8",
    )
    (output_path / "high_tension_edges.md").write_text(
        _render_high_tension_edges(edge_rows),
        encoding="utf-8",
    )
    return output_path


def _render_node_note(graph: Graph, node: Node, edge_rows: list[dict[str, Any]]) -> str:
    outgoing = [edge for edge in graph.outgoing_edges(node.id)]
    incoming = [edge for edge in graph.incoming_edges(node.id)]
    outgoing_tension = [
        row
        for row in edge_rows
        if row["source"] == node.id
    ]
    incoming_tension = [
        row
        for row in edge_rows
        if row["target"] == node.id
    ]
    return "\n".join(
        [
            f"# {node.label}",
            "",
            "## Node",
            "",
            f"- Node id: `{node.id}`",
            f"- Activation: {node.activation:.6f}",
            f"- Stability: {node.stability:.6f}",
            "",
            "## Metadata",
            "",
            "```yaml",
            _yaml_block(node.metadata),
            "```",
            "",
            "## Outgoing Edges",
            "",
            _render_node_edges(outgoing, direction="outgoing"),
            "",
            "## Incoming Edges",
            "",
            _render_node_edges(incoming, direction="incoming"),
            "",
            "## Current Tension Contributions",
            "",
            "Outgoing:",
            "",
            _render_tension_rows(outgoing_tension),
            "",
            "Incoming:",
            "",
            _render_tension_rows(incoming_tension),
            "",
        ]
    )


def _render_index(graph: Graph) -> str:
    lines = [
        "# CIG Obsidian Export",
        "",
        f"- Nodes: {len(graph.nodes)}",
        f"- Edges: {len(graph.edges)}",
        f"- Total tension: {total_tension(graph):.6f}",
        "",
        "## Nodes",
        "",
    ]
    lines.extend(
        f"- [[{node_id}|{node.label}]]"
        for node_id, node in graph.nodes.items()
    )
    lines.extend(
        [
            "",
            "## Graph Tables",
            "",
            "- [[edges]]",
            "- [[high_tension_edges]]",
            "",
        ]
    )
    return "\n".join(lines)


def _render_edges(edge_rows: list[dict[str, Any]]) -> str:
    return "\n".join(
        [
            "# Edges",
            "",
            "| Source | Relation | Target | Weight | Polarity | Expected Ratio | Tension |",
            "| --- | --- | --- | ---: | ---: | ---: | ---: |",
            *[
                (
                    f"| [[{row['source']}]] | {row['relation']} | [[{row['target']}]] | "
                    f"{row['weight']:.6f} | {row['polarity']:.6f} | "
                    f"{row['expected_ratio']:.6f} | {row['tension']:.6f} |"
                )
                for row in edge_rows
            ],
            "",
        ]
    )


def _render_high_tension_edges(edge_rows: list[dict[str, Any]]) -> str:
    sorted_rows = sorted(edge_rows, key=lambda row: (-row["tension"], row["index"]))
    nonzero_rows = [row for row in sorted_rows if row["tension"] > 0.0]
    rows = nonzero_rows or sorted_rows
    lines = [
        "# High Tension Edges",
        "",
    ]
    if not nonzero_rows:
        lines.extend(
            [
                "No nonzero edge tension in the current graph state.",
                "",
            ]
        )
    lines.extend(
        [
            "| Source | Relation | Target | Tension |",
            "| --- | --- | --- | ---: |",
            *[
                (
                    f"| [[{row['source']}]] | {row['relation']} | "
                    f"[[{row['target']}]] | {row['tension']:.6f} |"
                )
                for row in rows[:25]
            ],
            "",
        ]
    )
    return "\n".join(lines)


def _render_node_edges(edges: list[Edge], direction: str) -> str:
    if not edges:
        return "_None._"

    lines = []
    for edge in edges:
        if direction == "outgoing":
            lines.append(
                f"- {edge.relation}: [[{edge.target}]] "
                f"(weight={edge.weight:.3f}, polarity={edge.polarity:.3f})"
            )
        else:
            lines.append(
                f"- [[{edge.source}]]: {edge.relation} "
                f"(weight={edge.weight:.3f}, polarity={edge.polarity:.3f})"
            )
    return "\n".join(lines)


def _render_tension_rows(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_None._"

    lines = [
        "| Edge | Tension |",
        "| --- | ---: |",
    ]
    lines.extend(
        (
            f"| [[{row['source']}]] -> [[{row['target']}]] "
            f"({row['relation']}) | {row['tension']:.6f} |"
        )
        for row in sorted(rows, key=lambda item: (-item["tension"], item["index"]))
    )
    return "\n".join(lines)


def _edge_rows(graph: Graph) -> list[dict[str, Any]]:
    return [
        {
            "index": index,
            "source": edge.source,
            "target": edge.target,
            "relation": edge.relation,
            "weight": edge.weight,
            "polarity": edge.polarity,
            "expected_ratio": edge.expected_ratio,
            "tension": edge_tension(graph, edge),
        }
        for index, edge in enumerate(graph.edges)
    ]


def _yaml_block(value: dict[str, Any]) -> str:
    if not value:
        return "{}"
    return yaml.safe_dump(value, sort_keys=True).rstrip()
