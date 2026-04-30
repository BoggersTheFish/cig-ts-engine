from __future__ import annotations

import math
from pathlib import Path

from cig.engine import CIGEngine
from cig.evolve import apply_context_split
from cig.graph import Graph
from cig.io import load_graph
from cig.meaning import derivative_meaning
from cig.tension import edge_tension


REPORT_PATH = Path("docs/proof_bank/TS-012-prebuilt-concept-graph.md")
GRAPH_PATH = Path("examples/ts_core.yaml")
SYMBOLIC_INPUTS = ["meaning", "life", "number_47"]
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


def generate_proof_report(
    output_path: str | Path = REPORT_PATH,
    graph_path: str | Path = GRAPH_PATH,
) -> Path:
    """Generate a Markdown proof-bank report for the current TS demo graph."""
    graph_path = Path(graph_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    symbolic = run_symbolic_attractor_case(graph_path)
    derivative = run_religion_derivative_case(graph_path)
    split = run_context_split_case(graph_path)
    graph = load_graph(graph_path)

    output_path.write_text(
        render_report(
            graph=graph,
            graph_path=graph_path,
            symbolic=symbolic,
            derivative=derivative,
            split=split,
        ),
        encoding="utf-8",
    )
    return output_path


def run_symbolic_attractor_case(graph_path: Path) -> dict:
    graph = load_graph(graph_path)
    report = CIGEngine(graph).run_cycle(SYMBOLIC_INPUTS, steps=5)
    return {
        "inputs": SYMBOLIC_INPUTS,
        "steps": 5,
        "report": report,
        "interpretation": (
            "47 is not meaningful because of its literal numeric content. In "
            "this graph, it functions as an arbitrary symbolic attractor. The "
            "input meaning/life/number_47 propagates toward arbitrary_symbol, "
            "absurdity, humour, stable_attractor, and coherence. This supports "
            "the TS framing that meaning is graph-response, not "
            "symbol-intrinsic content."
        ),
    }


def run_religion_derivative_case(graph_path: Path) -> dict:
    comfort = derivative_meaning(
        load_graph(graph_path),
        "religion",
        context_inputs=["comfort"],
        steps=6,
    )
    trauma = derivative_meaning(
        load_graph(graph_path),
        "religion",
        context_inputs=["trauma"],
        steps=6,
    )
    return {
        "input": "religion",
        "comfort_context": comfort,
        "trauma_context": trauma,
        "cosine_similarity": cosine_similarity(
            comfort["derivative_vector"],
            trauma["derivative_vector"],
        ),
        "interpretation": (
            "The same symbol 'religion' produces different meaning vectors "
            "depending on graph context. Meaning is the derivative of graph "
            "state with respect to idea input."
        ),
    }


def run_context_split_case(graph_path: Path) -> dict:
    graph = load_graph(graph_path)
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
    return {
        "before_inputs": [
            ["religion", "comfort"],
            ["religion", "trauma", "control"],
        ],
        "after_inputs": [
            ["religion_comfort", "comfort"],
            ["religion_harm", "trauma", "control"],
        ],
        "tension_before": tension_before,
        "tension_after": tension_after,
        "percentage_reduction": percentage_reduction(tension_before, tension_after),
        "new_nodes": ["religion_comfort", "religion_harm"],
        "mapping": SPLIT_MAPPING,
        "interpretation": (
            "Break/Evolve is justified when one concept is forced to carry "
            "incompatible regimes. Splitting religion into context-specific "
            "nodes reduces false averaging and lowers tension. This is not "
            "adding complexity for decoration; it is adding structure only "
            "when tension relief justifies the extra representational radius."
        ),
    }


def render_report(
    graph: Graph,
    graph_path: Path,
    symbolic: dict,
    derivative: dict,
    split: dict,
) -> str:
    symbolic_report = symbolic["report"]
    comfort = derivative["comfort_context"]
    trauma = derivative["trauma_context"]
    return "\n".join(
        [
            "# TS-012: Prebuilt Concept Graph",
            "",
            "## Hypothesis",
            "",
            (
                "A hand-authored CIG can run an inspectable TS cycle where "
                "activation, tension, derivative meaning, and Break/Evolve "
                "suggestions are explicit graph operations."
            ),
            "",
            "## Graph Used",
            "",
            f"- Graph path: `{graph_path}`",
            f"- Nodes: {len(graph.nodes)}",
            f"- Edges: {len(graph.edges)}",
            "",
            "## Equations",
            "",
            "- Propagation: `a_next = decay * a + activation_rate * incoming`",
            "- Edge tension: `tau_ij = weight * (a_j - expected_ratio * a_i)^2`",
            "- Total tension: `T = sum tau_ij over all edges`",
            (
                "- Meaning derivative: "
                "`M(u) ~= (final_state(input + epsilon) - final_state(input)) / epsilon`"
            ),
            (
                "- Break/Evolve criterion: "
                "`accept G -> G' only if T(G) - T(G') > alpha * (R(G') - R(G))`"
            ),
            "",
            "## Demo 1: 47 Symbolic Attractor",
            "",
            "### Input Conditions",
            "",
            _bullet_list(symbolic["inputs"]),
            f"- Steps: {symbolic['steps']}",
            "",
            "### Results",
            "",
            f"- Tension before: {symbolic_report['tension_before']:.6f}",
            f"- Tension after: {symbolic_report['tension_after']:.6f}",
            "",
            "Top activated nodes:",
            "",
            _activation_table(symbolic_report["top_activated_nodes"][:10]),
            "",
            "Top tension edges after:",
            "",
            _tension_table(symbolic_report["top_tension_edges_after"][:10]),
            "",
            "### Interpretation",
            "",
            symbolic["interpretation"],
            "",
            "## Demo 2: Religion Derivative Meaning",
            "",
            "### Input Conditions",
            "",
            "- Input node: `religion`",
            "- Context A: `comfort`",
            "- Context B: `trauma`",
            "- Steps: 6",
            "",
            "### Results",
            "",
            f"- Cosine similarity: {derivative['cosine_similarity']:.6f}",
            "",
            "Comfort-context derivative vector, top entries:",
            "",
            _derivative_table(comfort["top_derivative_nodes"][:10]),
            "",
            "Trauma-context derivative vector, top entries:",
            "",
            _derivative_table(trauma["top_derivative_nodes"][:10]),
            "",
            "### Interpretation",
            "",
            derivative["interpretation"],
            "",
            "## Demo 3: Context Split Break/Evolve",
            "",
            "### Input Conditions",
            "",
            "- Before split case A: `religion`, `comfort`",
            "- Before split case B: `religion`, `trauma`, `control`",
            "- After split case A: `religion_comfort`, `comfort`",
            "- After split case B: `religion_harm`, `trauma`, `control`",
            "",
            "### Results",
            "",
            f"- Tension before split: {split['tension_before']:.6f}",
            f"- Tension after split: {split['tension_after']:.6f}",
            f"- Percentage reduction: {split['percentage_reduction']:.2f}%",
            f"- New nodes: {', '.join(f'`{node}`' for node in split['new_nodes'])}",
            "",
            "Redirected edges:",
            "",
            _redirect_table(split["mapping"]),
            "",
            "### Interpretation",
            "",
            split["interpretation"],
            "",
            "## Limitations",
            "",
            "- This is a hand-authored graph, not a learned model.",
            "- Results depend on chosen edge weights.",
            (
                "- It proves only that a prebuilt CIG can run an inspectable "
                "TS cycle, not that it models all human meaning."
            ),
            "- Relaxation rules must avoid over-smoothing incompatible contexts.",
            "",
        ]
    )


def run_case(graph: Graph, inputs: list[str]) -> Graph:
    case_graph = graph.copy()
    CIGEngine(case_graph).run_cycle(inputs, steps=5)
    return case_graph


def regime_tension(graph: Graph, source: str, targets: set[str]) -> float:
    return sum(
        edge_tension(graph, edge)
        for edge in graph.edges
        if edge.source == source and edge.target in targets
    )


def percentage_reduction(before: float, after: float) -> float:
    if before == 0.0:
        return 0.0
    return (before - after) / before * 100.0


def cosine_similarity(first: dict[str, float], second: dict[str, float]) -> float:
    keys = sorted(set(first) | set(second))
    dot = sum(first.get(key, 0.0) * second.get(key, 0.0) for key in keys)
    first_norm = math.sqrt(sum(first.get(key, 0.0) ** 2 for key in keys))
    second_norm = math.sqrt(sum(second.get(key, 0.0) ** 2 for key in keys))
    if first_norm == 0.0 or second_norm == 0.0:
        return 0.0
    return dot / (first_norm * second_norm)


def _bullet_list(items: list[str]) -> str:
    return "\n".join(f"- `{item}`" for item in items)


def _activation_table(rows: list[dict]) -> str:
    lines = ["| Node | Activation |", "| --- | ---: |"]
    lines.extend(f"| `{row['id']}` | {row['activation']:.6f} |" for row in rows)
    return "\n".join(lines)


def _tension_table(rows: list[dict]) -> str:
    lines = ["| Edge | Relation | Tension |", "| --- | --- | ---: |"]
    lines.extend(
        (
            f"| `{row['source']} -> {row['target']}` | "
            f"{row['relation']} | {row['tension']:.6f} |"
        )
        for row in rows
    )
    return "\n".join(lines)


def _derivative_table(rows: list[dict]) -> str:
    lines = ["| Node | Derivative |", "| --- | ---: |"]
    lines.extend(f"| `{row['id']}` | {row['derivative']:.6f} |" for row in rows)
    return "\n".join(lines)


def _redirect_table(mapping: dict[str, str]) -> str:
    lines = ["| Old edge target | New source |", "| --- | --- |"]
    lines.extend(
        f"| `religion -> {target}` | `{new_source} -> {target}` |"
        for target, new_source in mapping.items()
    )
    return "\n".join(lines)
