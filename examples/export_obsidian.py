from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from cig.io import load_graph
from cig.obsidian import export_obsidian


def main() -> None:
    graph = load_graph(PROJECT_ROOT / "examples/ts_core.yaml")
    output_dir = export_obsidian(graph, PROJECT_ROOT / "obsidian_export")
    print(f"wrote: {output_dir}")


if __name__ == "__main__":
    main()
