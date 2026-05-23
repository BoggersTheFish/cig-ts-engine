# cig-ts-engine

**Status:** active experimental prototype.

**Canonical route:** [TS-Start-Here](https://github.com/BoggersTheFish/TS-Start-Here) -> [TS-Reasoner-v0](https://github.com/BoggersTheFish/TS-Reasoner-v0) -> [TensionLM](https://github.com/BoggersTheFish/TensionLM) -> TS-Codex-OS / TS-Core / CIG.

**Role in the TS stack:** Compact CIG/TS engine for claim/evidence graph dynamics, confidence, contradiction tracking, and inspectable knowledge state.

**What this repo is:** A local-first Python runtime for deterministic Concept/Constraint Intelligence Graph experiments with explicit graph state and TS-style tension cycles.

**What this repo is not:** Not a production knowledge base or finished autonomous reasoner.

**Start here:** install the editable package, run tests, then inspect the CIG/TS cycle examples below.

## CIG/TS Engine

A local-first Python runtime for experimenting with a deterministic
Concept/Constraint Intelligence Graph (CIG) and Thinking System (TS).

This project is not an LLM wrapper. The reasoning state is an explicit graph:
nodes carry activation, edges carry weighted relations or constraints, and the
engine runs deterministic propagation, tension measurement, derivative probes,
and simple Break/Evolve suggestions.

The current repository is a small prebuilt graph and runtime. It demonstrates
that an inspectable graph can run TS-style cycles; it does not claim to model
all human meaning.

## CIG/TS In Short

- CIG: a graph of concepts, claims, symbols, memories, and states.
- TS: a deterministic cycle over that graph.
- Node: a graph item with activation, stability, and metadata.
- Edge: a directed weighted relation or constraint between nodes.
- Meaning: measured here as graph response to an input perturbation.
- Break/Evolve: a proposed graph restructure when tension relief justifies
  added representational cost.

Core cycle:

```text
Propagate -> Relax -> Detect Tension -> Break/Evolve
```

## Mathematical Definitions

Activation update:

```text
a_next = decay * a + activation_rate * incoming
```

Edge contribution during propagation:

```text
contribution = source_activation * weight * polarity * activation_rate
```

Edge tension:

```text
tau_ij = weight * (a_j - expected_ratio * a_i)^2
```

Total tension:

```text
T = sum tau_ij over all edges
```

Meaning derivative:

```text
M(u) ~= (final_state(input + epsilon) - final_state(input)) / epsilon
```

Representational radius:

```text
R(graph) = sum primitive_cost + beta * edge_count
```

Break/Evolve acceptance rule:

```text
accept G -> G' only if T(G) - T(G') > alpha * (R(G') - R(G))
```

## Installation

Use Python 3.11 or newer.

```bash
python -m pip install -e ".[dev]"
```

If your environment exposes Python as `python3` instead of `python`, use:

```bash
python3 -m pip install -e ".[dev]"
```

The editable install provides the `cig` CLI.

## Run Tests

```bash
pytest
```

or:

```bash
python -m pytest
```

## CLI Commands

Run a propagation cycle:

```bash
cig run examples/ts_core.yaml --input meaning --input life --input number_47 --steps 6
```

Inspect graph tension:

```bash
cig tension examples/ts_core.yaml
```

Compute derivative meaning:

```bash
cig derivative examples/ts_core.yaml --input religion --context comfort --steps 6
```

Inspect evolve suggestions:

```bash
cig evolve examples/ts_core.yaml --node religion
```

Render a graph PNG:

```bash
cig visualize examples/ts_core.yaml --output examples/ts_core.png
```

## Demos

47 symbolic attractor:

```bash
python examples/run_47_demo.py
```

Religion derivative meaning:

```bash
python examples/run_religion_derivative_demo.py
```

Context split Break/Evolve:

```bash
python examples/run_context_split_demo.py
```

Generate the proof-bank report:

```bash
python examples/generate_proof_report.py
```

Export an Obsidian vault:

```bash
python examples/export_obsidian.py
```

If your shell does not provide a `python` command, replace `python` with the
interpreter for your environment, for example `python3` or a virtualenv path.

## Repository Layout

- `src/cig/`: runtime package
- `examples/ts_core.yaml`: hand-authored seed graph
- `examples/*.py`: runnable demos and exporters
- `docs/proof_bank/`: generated proof-bank Markdown report
- `obsidian_export/`: generated Obsidian vault export
- `tests/`: pytest coverage for graph models, IO, propagation, tension,
  derivative meaning, compression radius, evolve suggestions, and CLI smoke
  tests

## Limitations

- The included graph is hand-authored, not learned.
- Results depend on chosen edge weights and metadata.
- Current propagation and relaxation rules are deliberately simple.
- The demos show inspectable graph mechanics, not a general theory of human
  meaning.

## License

MIT. See [LICENSE](LICENSE).
