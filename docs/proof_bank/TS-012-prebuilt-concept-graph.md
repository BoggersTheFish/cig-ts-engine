# TS-012: Prebuilt Concept Graph

## Hypothesis

A hand-authored CIG can run an inspectable TS cycle where activation, tension, derivative meaning, and Break/Evolve suggestions are explicit graph operations.

## Graph Used

- Graph path: `/home/boggersthefish/Desktop/cig-ts-engine/examples/ts_core.yaml`
- Nodes: 27
- Edges: 33

## Equations

- Propagation: `a_next = decay * a + activation_rate * incoming`
- Edge tension: `tau_ij = weight * (a_j - expected_ratio * a_i)^2`
- Total tension: `T = sum tau_ij over all edges`
- Meaning derivative: `M(u) ~= (final_state(input + epsilon) - final_state(input)) / epsilon`
- Break/Evolve criterion: `accept G -> G' only if T(G) - T(G') > alpha * (R(G') - R(G))`

## Demo 1: 47 Symbolic Attractor

### Input Conditions

- `meaning`
- `life`
- `number_47`
- Steps: 5

### Results

- Tension before: 1.398625
- Tension after: 1.154088

Top activated nodes:

| Node | Activation |
| --- | ---: |
| `arbitrary_symbol` | 1.000000 |
| `life` | 1.000000 |
| `meaning` | 1.000000 |
| `number_47` | 1.000000 |
| `stable_attractor` | 1.000000 |
| `coherence` | 0.775308 |
| `absurdity` | 0.665190 |
| `humour` | 0.192700 |

Top tension edges after:

| Edge | Relation | Tension |
| --- | --- | ---: |
| `comfort -> stable_attractor` | stabilizes | 0.550000 |
| `relaxation -> coherence` | supports | 0.300551 |
| `arbitrary_symbol -> stable_attractor` | can_settle_into | 0.112500 |
| `absurdity -> humour` | evokes | 0.086421 |
| `life -> meaning` | raises_question_of | 0.053125 |
| `meaning -> stable_attractor` | seeks | 0.036000 |
| `number_47 -> arbitrary_symbol` | exemplifies | 0.009500 |
| `stable_attractor -> coherence` | stabilizes | 0.005021 |
| `arbitrary_symbol -> absurdity` | evokes | 0.000969 |
| `religion -> ritual` | organizes | 0.000000 |

### Interpretation

47 is not meaningful because of its literal numeric content. In this graph, it functions as an arbitrary symbolic attractor. The input meaning/life/number_47 propagates toward arbitrary_symbol, absurdity, humour, stable_attractor, and coherence. This supports the TS framing that meaning is graph-response, not symbol-intrinsic content.

## Demo 2: Religion Derivative Meaning

### Input Conditions

- Input node: `religion`
- Context A: `comfort`
- Context B: `trauma`
- Steps: 6

### Results

- Cosine similarity: 0.001430

Comfort-context derivative vector, top entries:

| Node | Derivative |
| --- | ---: |
| `ritual` | 0.116016 |
| `community` | 0.100486 |
| `trauma` | 0.007765 |

Trauma-context derivative vector, top entries:

| Node | Derivative |
| --- | ---: |
| `tension` | 0.240368 |
| `control` | 0.132002 |
| `trauma` | 0.007765 |

### Interpretation

The same symbol 'religion' produces different meaning vectors depending on graph context. Meaning is the derivative of graph state with respect to idea input.

## Demo 3: Context Split Break/Evolve

### Input Conditions

- Before split case A: `religion`, `comfort`
- Before split case B: `religion`, `trauma`, `control`
- After split case A: `religion_comfort`, `comfort`
- After split case B: `religion_harm`, `trauma`, `control`

### Results

- Tension before split: 1.748551
- Tension after split: 0.576247
- Percentage reduction: 67.04%
- New nodes: `religion_comfort`, `religion_harm`

Redirected edges:

| Old edge target | New source |
| --- | --- |
| `religion -> comfort` | `religion_comfort -> comfort` |
| `religion -> ritual` | `religion_comfort -> ritual` |
| `religion -> community` | `religion_comfort -> community` |
| `religion -> control` | `religion_harm -> control` |
| `religion -> trauma` | `religion_harm -> trauma` |
| `religion -> tension` | `religion_harm -> tension` |

### Interpretation

Break/Evolve is justified when one concept is forced to carry incompatible regimes. Splitting religion into context-specific nodes reduces false averaging and lowers tension. This is not adding complexity for decoration; it is adding structure only when tension relief justifies the extra representational radius.

## Limitations

- This is a hand-authored graph, not a learned model.
- Results depend on chosen edge weights.
- It proves only that a prebuilt CIG can run an inspectable TS cycle, not that it models all human meaning.
- Relaxation rules must avoid over-smoothing incompatible contexts.
