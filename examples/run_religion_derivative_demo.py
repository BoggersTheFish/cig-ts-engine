from __future__ import annotations

import math
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from cig.io import load_graph
from cig.meaning import derivative_meaning


EXPLANATION = (
    "The same symbol 'religion' produces different meaning vectors depending "
    "on graph context. In the comfort context, derivative response should lean "
    "toward ritual, comfort, community, stable_attractor, coherence, or "
    "relaxation if present. In the trauma context, derivative response should "
    "lean toward control, tension, trauma, or harm-related nodes. Meaning is "
    "the derivative of graph state with respect to idea input."
)


def main() -> None:
    graph_path = Path(__file__).with_name("ts_core.yaml")
    comfort_report = derivative_meaning(
        load_graph(graph_path),
        "religion",
        context_inputs=["comfort"],
    )
    trauma_report = derivative_meaning(
        load_graph(graph_path),
        "religion",
        context_inputs=["trauma"],
    )
    similarity = cosine_similarity(
        comfort_report["derivative_vector"],
        trauma_report["derivative_vector"],
    )

    print("Religion Derivative Meaning Demo")
    print("=" * 33)
    print()
    print("Input symbol: religion")
    print()
    print("Comfort context top derivative nodes:")
    print_top_derivatives(comfort_report)
    print()
    print("Trauma context top derivative nodes:")
    print_top_derivatives(trauma_report)
    print()
    print(f"Cosine similarity: {similarity:.6f}")
    print()
    print("TS explanation:")
    print(EXPLANATION)


def print_top_derivatives(report: dict, limit: int = 8) -> None:
    for node in report["top_derivative_nodes"][:limit]:
        print(f"- {node['id']}: {node['derivative']:.6f}")


def cosine_similarity(first: dict[str, float], second: dict[str, float]) -> float:
    keys = sorted(set(first) | set(second))
    dot = sum(first.get(key, 0.0) * second.get(key, 0.0) for key in keys)
    first_norm = math.sqrt(sum(first.get(key, 0.0) ** 2 for key in keys))
    second_norm = math.sqrt(sum(second.get(key, 0.0) ** 2 for key in keys))
    if first_norm == 0.0 or second_norm == 0.0:
        return 0.0
    return dot / (first_norm * second_norm)


if __name__ == "__main__":
    main()
