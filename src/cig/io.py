from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from cig.graph import Graph


def load_graph_yaml(path: str | Path) -> Graph:
    with Path(path).open("r", encoding="utf-8") as handle:
        payload: dict[str, Any] = yaml.safe_load(handle) or {}
    return graph_from_mapping(payload)


def graph_from_mapping(payload: dict[str, Any]) -> Graph:
    nodes = payload.get("nodes", [])
    edges = payload.get("edges", [])
    if not isinstance(nodes, list):
        raise TypeError("nodes must be a list")
    if not isinstance(edges, list):
        raise TypeError("edges must be a list")
    return Graph.from_records(nodes=nodes, edges=edges)

