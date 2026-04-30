# Control

## Node

- Node id: `control`
- Activation: 0.000000
- Stability: 1.000000

## Metadata

```yaml
type: concept
```

## Outgoing Edges

- increases: [[tension]] (weight=0.850, polarity=1.000)

## Incoming Edges

- [[religion]]: can_enable (weight=0.850, polarity=1.000)
- [[comfort]]: softens (weight=1.000, polarity=-1.000)

## Current Tension Contributions

Outgoing:

| Edge | Tension |
| --- | ---: |
| [[control]] -> [[tension]] (increases) | 0.000000 |

Incoming:

| Edge | Tension |
| --- | ---: |
| [[religion]] -> [[control]] (can_enable) | 0.000000 |
| [[comfort]] -> [[control]] (softens) | 0.000000 |
