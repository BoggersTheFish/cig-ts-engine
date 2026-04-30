# Comfort

## Node

- Node id: `comfort`
- Activation: 0.000000
- Stability: 1.000000

## Metadata

```yaml
type: state
```

## Outgoing Edges

- stabilizes: [[stable_attractor]] (weight=0.550, polarity=1.000)
- supports: [[relaxation]] (weight=0.550, polarity=1.000)
- softens: [[control]] (weight=1.000, polarity=-1.000)
- relaxes: [[tension]] (weight=0.800, polarity=-1.000)

## Incoming Edges

- [[ritual]]: supports (weight=0.700, polarity=1.000)
- [[religion]]: can_support (weight=0.600, polarity=1.000)
- [[community]]: supports (weight=0.350, polarity=1.000)
- [[trauma]]: disrupts (weight=1.300, polarity=-1.000)

## Current Tension Contributions

Outgoing:

| Edge | Tension |
| --- | ---: |
| [[comfort]] -> [[stable_attractor]] (stabilizes) | 0.000000 |
| [[comfort]] -> [[relaxation]] (supports) | 0.000000 |
| [[comfort]] -> [[control]] (softens) | 0.000000 |
| [[comfort]] -> [[tension]] (relaxes) | 0.000000 |

Incoming:

| Edge | Tension |
| --- | ---: |
| [[ritual]] -> [[comfort]] (supports) | 0.000000 |
| [[religion]] -> [[comfort]] (can_support) | 0.000000 |
| [[community]] -> [[comfort]] (supports) | 0.000000 |
| [[trauma]] -> [[comfort]] (disrupts) | 0.000000 |
