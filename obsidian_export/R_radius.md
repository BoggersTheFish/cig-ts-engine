# R Radius

## Node

- Node id: `R_radius`
- Activation: 0.000000
- Stability: 1.000000

## Metadata

```yaml
type: metric
```

## Outgoing Edges

- defines_objective_for: [[minimum_R_compressor]] (weight=0.900, polarity=-1.000)

## Incoming Edges

- [[compression]]: minimizes (weight=0.800, polarity=-1.000)

## Current Tension Contributions

Outgoing:

| Edge | Tension |
| --- | ---: |
| [[R_radius]] -> [[minimum_R_compressor]] (defines_objective_for) | 0.000000 |

Incoming:

| Edge | Tension |
| --- | ---: |
| [[compression]] -> [[R_radius]] (minimizes) | 0.000000 |
