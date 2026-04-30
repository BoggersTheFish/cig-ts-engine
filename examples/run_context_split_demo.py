from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from cig.engine import CIGEngine
from cig.evolve import apply_context_split
from cig.io import load_graph
from cig.tension import edge_tension


COMFORT_TARGETS = {"comfort", "ritual", "community"}
HARM_TARGETS = {"control", "trauma", "tension"}
SPLIT_MAPPING = {
    "comfort": "religion_comfort",
    "ritual": "religion_comfort",
    "community": "religion_comfort",
    "control": "religion_harm",
    "trauma": "religion_harm",
    "tension": "religion_harm",
}
EXPLANATION = (
    "Break/Evolve is justified when one concept is forced to carry "
    "incompatible regimes. Splitting religion into context-specific nodes "
    "reduces false averaging and lowers tension. This is not adding "
    "complexity for decoration; it is adding structure only when tension "
    "relief justifies the extra representational radius."
)


def main() -> None:
    graph = load_graph(Path(__file__).with_name("ts_core.yaml"))

    before_comfort = run_case(graph, ["religion", "comfort"])
    before_harm = run_case(graph, ["religion", "trauma", "control"])
    tension_before = (
        regime_tension(before_comfort, "religion", COMFORT_TARGETS | HARM_TARGETS)
        + regime_tension(before_harm, "religion", COMFORT_TARGETS | HARM_TARGETS)
    )

    split_graph = apply_context_split(graph, "religion", SPLIT_MAPPING)
    after_comfort = run_case(split_graph, ["religion_comfort", "comfort"])
    after_harm = run_case(split_graph, ["religion_harm", "trauma", "control"])
    tension_after = (
        regime_tension(after_comfort, "religion_comfort", COMFORT_TARGETS)
        + regime_tension(after_harm, "religion_harm", HARM_TARGETS)
    )
    reduction = percentage_reduction(tension_before, tension_after)

    print("Religion Context Split Demo")
    print("===========================")
    print()
    print(f"Tension before split: {tension_before:.6f}")
    print(f"Tension after split:  {tension_after:.6f}")
    print(f"Percentage reduction: {reduction:.2f}%")
    print()
    print("New nodes:")
    print("- religion_comfort")
    print("- religion_harm")
    print()
    print("Redirected edges:")
    for target, new_source in SPLIT_MAPPING.items():
        print(f"- religion -> {target} becomes {new_source} -> {target}")
    print()
    print("Explanation:")
    print(EXPLANATION)


def run_case(graph, inputs: list[str]):
    case_graph = graph.copy()
    CIGEngine(case_graph).run_cycle(inputs, steps=5)
    return case_graph


def regime_tension(graph, source: str, targets: set[str]) -> float:
    return sum(
        edge_tension(graph, edge)
        for edge in graph.edges
        if edge.source == source and edge.target in targets
    )


def percentage_reduction(before: float, after: float) -> float:
    if before == 0.0:
        return 0.0
    return (before - after) / before * 100.0


if __name__ == "__main__":
    main()
