from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from cig.engine import CIGEngine
from cig.io import load_graph


INPUT_NODES = ["meaning", "life", "number_47"]

INTERPRETATION = (
    "47 is not meaningful because of its literal numeric content. In this "
    "graph, it functions as an arbitrary symbolic attractor. The input "
    "meaning/life/number_47 propagates toward arbitrary_symbol, absurdity, "
    "humour, stable_attractor, and coherence. This supports the TS framing "
    "that meaning is graph-response, not symbol-intrinsic content."
)


def main() -> None:
    graph = load_graph(Path(__file__).with_name("ts_core.yaml"))
    report = CIGEngine(graph).run_cycle(INPUT_NODES, steps=5)

    print("47 TS Demo")
    print("=" * 10)
    print()
    print("Input nodes:")
    for node_id in report["input_nodes"]:
        print(f"- {node_id}")

    print()
    print("Top activated nodes:")
    for node in report["top_activated_nodes"][:10]:
        print(f"- {node['id']}: {node['activation']:.4f}")

    print()
    print(f"Tension before: {report['tension_before']:.6f}")
    print(f"Tension after:  {report['tension_after']:.6f}")

    print()
    print("Top tension edges after:")
    for edge in report["top_tension_edges_after"][:10]:
        print(
            f"- {edge['source']} -> {edge['target']} "
            f"({edge['relation']}): {edge['tension']:.6f}"
        )

    print()
    print("TS interpretation:")
    print(INTERPRETATION)


if __name__ == "__main__":
    main()
