This repository implements a deterministic Concept/Constraint Intelligence Graph engine for TS.

Do not treat an LLM as the reasoning core.
The reasoning core is the graph.

Core TS definitions:
- Nodes are concepts, claims, memories, symbols, or states.
- Edges are weighted relations, constraints, evidence links, contradictions, or transformations.
- Activation is current signal strength.
- Tension is unresolved constraint error.
- Coherence is low-tension graph stability.
- Meaning is the derivative of graph state with respect to idea input.
- Break/Evolve is allowed only when tension reduction justifies added complexity.
- R means representational / axiomatic radius: the size or cost of primitive assumptions needed by a system.
- TS aims to be a minimum-R information compressor for human ideas.

Core cycle:
Propagate -> Relax -> Detect Tension -> Break/Evolve.

Implementation rules:
1. Prefer explicit graph rules over hidden model behaviour.
2. Keep everything inspectable and deterministic by default.
3. Log tension before and after every cycle.
4. Add tests for every new TS claim.
5. Preserve provenance for graph edits where possible.
6. Keep symbolic/narrative framing separate from technical claims.
7. Do not add vague metaphysics to public docs.
8. Every demo should show input, activated nodes, tension before, tension after, and interpretation.
9. Avoid graph bloat. Evolve only when tension reduction beats complexity cost.
10. The LLM/Codex is the builder/operator. The CIG graph is the reasoning structure.

Mathematical core:
- Propagation:
  a_next = decay * a + activation_rate * incoming
- Edge tension:
  tau_ij = weight * (a_j - expected_ratio * a_i)^2
- Total tension:
  T = sum tau_ij over all edges
- Meaning derivative:
  M(u) ~= (final_state(input + epsilon) - final_state(input)) / epsilon
- Break/Evolve criterion:
  accept G -> G' only if T(G) - T(G') > alpha * (R(G') - R(G))

Project goal:
Build a local-first CIG/TS runtime that can run TS reasoning cycles from hand-authored YAML graphs before any model training.
