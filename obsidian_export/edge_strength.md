# Edge Strength

## Node

- Node id: `edge_strength`
- Activation: 0.000000
- Stability: 1.000000

## Metadata

```yaml
type: constraint
```

## Outgoing Edges

- shapes: [[derivative_response]] (weight=0.750, polarity=1.000)

## Incoming Edges

- [[graph]]: parameterizes (weight=0.800, polarity=1.000)

## Current Tension Contributions

Outgoing:

| Edge | Tension |
| --- | ---: |
| [[edge_strength]] -> [[derivative_response]] (shapes) | 0.000000 |

Incoming:

| Edge | Tension |
| --- | ---: |
| [[graph]] -> [[edge_strength]] (parameterizes) | 0.000000 |
