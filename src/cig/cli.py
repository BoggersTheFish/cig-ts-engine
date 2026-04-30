from __future__ import annotations

from pathlib import Path

import typer

from cig.io import load_graph_yaml

app = typer.Typer(help="CIG/TS engine command line tools.")


@app.command()
def inspect(path: Path) -> None:
    """Inspect a graph YAML file."""
    graph = load_graph_yaml(path)
    typer.echo(f"nodes={len(graph.nodes)} edges={len(graph.edges)}")


@app.command()
def step(path: Path) -> None:
    """Run one placeholder TS cycle and print tension."""
    from cig.engine import ThinkingSystemEngine

    graph = load_graph_yaml(path)
    report = ThinkingSystemEngine(graph).step()
    typer.echo(f"tension={report.total:.6f} coherence={report.coherence:.6f}")


if __name__ == "__main__":
    app()

