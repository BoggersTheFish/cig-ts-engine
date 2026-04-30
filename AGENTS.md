# CIG/TS Engine Agent Notes

This repository is a Python 3.11+ skeleton for a deterministic
Concept/Constraint Intelligence Graph (CIG) and Thinking System (TS) engine.

## Project Intent

The reasoning core is an explicit graph, not an LLM wrapper. Keep logic
deterministic, inspectable, and testable.

Core cycle:

```text
Propagate -> Relax -> Detect Tension -> Break/Evolve
```

## Development Guidelines

- Keep dependencies limited to those declared in `pyproject.toml`.
- Prefer explicit data models and deterministic state transitions.
- Do not introduce hidden network calls or LLM dependencies.
- Add tests for any concrete behavior beyond placeholders.
- Leave TODO comments where theory or algorithms are intentionally incomplete.

