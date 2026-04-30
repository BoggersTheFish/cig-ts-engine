from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from cig.engine import CIGEngine
from cig.evolve import find_overloaded_nodes, suggest_context_split
from cig.io import load_graph
from cig.meaning import derivative_meaning
from cig.tension import tension_report

app = typer.Typer(help="CIG/TS graph runtime CLI.")


@app.command()
def run(
    graph_path: Annotated[Path, typer.Argument(help="Path to a CIG YAML graph.")],
    input_nodes: Annotated[
        list[str],
        typer.Option("--input", help="Input node id. Repeat for multiple inputs."),
    ],
    steps: Annotated[int, typer.Option("--steps", help="Propagation steps.")] = 6,
) -> None:
    """Run propagation and print top activations plus tension."""
    if not input_nodes:
        raise typer.BadParameter("at least one --input is required")

    graph = load_graph(graph_path)
    report = CIGEngine(graph).run_cycle(input_nodes, steps=steps)

    typer.echo("CIG run")
    typer.echo(f"graph: {graph_path}")
    typer.echo(f"inputs: {', '.join(report['input_nodes'])}")
    typer.echo(f"steps: {report['steps']}")
    typer.echo(f"tension before: {report['tension_before']:.6f}")
    typer.echo(f"tension after:  {report['tension_after']:.6f}")
    typer.echo()
    typer.echo("top activations:")
    _print_activation_rows(report["top_activated_nodes"])
    typer.echo()
    typer.echo("top tension edges after:")
    _print_tension_rows(report["top_tension_edges_after"])


@app.command()
def tension(
    graph_path: Annotated[Path, typer.Argument(help="Path to a CIG YAML graph.")],
    top_k: Annotated[int, typer.Option("--top-k", help="Number of edges to show.")] = 10,
) -> None:
    """Print total tension and top tension edges."""
    graph = load_graph(graph_path)
    report = tension_report(graph, top_k=top_k)

    typer.echo("CIG tension")
    typer.echo(f"graph: {graph_path}")
    typer.echo(f"total tension: {report['total']:.6f}")
    typer.echo()
    typer.echo("top tension edges:")
    _print_tension_rows(report["top_edges"])


@app.command()
def derivative(
    graph_path: Annotated[Path, typer.Argument(help="Path to a CIG YAML graph.")],
    input_node: Annotated[str, typer.Option("--input", help="Input node id.")],
    context: Annotated[
        list[str],
        typer.Option("--context", help="Context node id. Repeat for multiple contexts."),
    ] = [],
    steps: Annotated[int, typer.Option("--steps", help="Propagation steps.")] = 6,
) -> None:
    """Print top derivative meaning vector entries."""
    graph = load_graph(graph_path)
    report = derivative_meaning(
        graph,
        input_node_id=input_node,
        context_inputs=context,
        steps=steps,
    )

    typer.echo("CIG derivative meaning")
    typer.echo(f"graph: {graph_path}")
    typer.echo(f"input: {report['input_node']}")
    typer.echo(f"context: {', '.join(report['context_inputs']) or '(none)'}")
    typer.echo(f"steps: {report['steps']}")
    typer.echo()
    typer.echo("top derivative nodes:")
    for node in report["top_derivative_nodes"][:10]:
        typer.echo(f"- {node['id']}: {node['derivative']:.6f}")


@app.command()
def evolve(
    graph_path: Annotated[Path, typer.Argument(help="Path to a CIG YAML graph.")],
    node: Annotated[str, typer.Option("--node", help="Node id to inspect.")],
) -> None:
    """Print overloaded node report and context split suggestion."""
    graph = load_graph(graph_path)
    overloaded = find_overloaded_nodes(graph, top_k=max(5, len(graph.nodes)))
    node_report = next((item for item in overloaded if item["node_id"] == node), None)

    typer.echo("CIG evolve")
    typer.echo(f"graph: {graph_path}")
    typer.echo(f"node: {node}")
    typer.echo()

    if node_report is None:
        typer.echo("overloaded node report: none")
    else:
        typer.echo("overloaded node report:")
        typer.echo(f"- outgoing edges: {node_report['outgoing_count']}")
        typer.echo(f"- outgoing tension: {node_report['outgoing_tension']:.6f}")
        typer.echo(f"- tension variation: {node_report['tension_variation']:.6f}")
        typer.echo(f"- target groups: {', '.join(node_report['target_groups'])}")
        typer.echo("- highest tension outgoing edges:")
        _print_overload_edge_rows(node_report["edges"])

    split_names = _default_split_names(node, node_report)
    suggestion = suggest_context_split(graph, node, split_names)
    typer.echo()
    typer.echo("context split suggestion:")
    typer.echo(f"- original node: {suggestion['original_node']['id']}")
    typer.echo(
        "- new nodes: "
        + ", ".join(item["id"] for item in suggestion["new_nodes"])
    )
    typer.echo(
        f"- delta_R: {suggestion['expected_complexity_increase_delta_R']:.1f}"
    )
    typer.echo("- redirects:")
    for item in suggestion["edges_to_redirect"]:
        typer.echo(
            f"  - {item['source']} -> {item['target']} becomes "
            f"{item['suggested_new_source']} -> {item['target']}"
        )
    typer.echo(f"- explanation: {suggestion['explanation']}")


def _print_activation_rows(rows: list[dict], limit: int = 10) -> None:
    for row in rows[:limit]:
        typer.echo(f"- {row['id']}: {row['activation']:.6f}")


def _print_tension_rows(rows: list[dict], limit: int = 10) -> None:
    for row in rows[:limit]:
        typer.echo(
            f"- {row['source']} -> {row['target']} "
            f"({row['relation']}): {row['tension']:.6f}"
        )


def _print_overload_edge_rows(rows: list[dict], limit: int = 10) -> None:
    for row in rows[:limit]:
        typer.echo(
            f"  - {row['source']} -> {row['target']} "
            f"({row['relation']}): {row['tension']:.6f}"
        )


def _default_split_names(node: str, node_report: dict | None) -> list[str]:
    if node == "religion":
        return ["religion_comfort", "religion_harm"]
    if node_report is None or len(node_report["target_groups"]) < 2:
        return [f"{node}_context_a", f"{node}_context_b"]
    return [
        f"{node}_{group}".replace(" ", "_")
        for group in node_report["target_groups"][:2]
    ]


if __name__ == "__main__":
    app()
