# Stable Attractor

## Node

- Node id: `stable_attractor`
- Activation: 0.000000
- Stability: 1.000000

## Metadata

```yaml
type: state
```

## Outgoing Edges

- stabilizes: [[coherence]] (weight=0.900, polarity=1.000)

## Incoming Edges

- [[arbitrary_symbol]]: can_settle_into (weight=0.450, polarity=1.000)
- [[meaning]]: seeks (weight=0.900, polarity=1.000)
- [[comfort]]: stabilizes (weight=0.550, polarity=1.000)

## Current Tension Contributions

Outgoing:

| Edge | Tension |
| --- | ---: |
| [[stable_attractor]] -> [[coherence]] (stabilizes) | 0.000000 |

Incoming:

| Edge | Tension |
| --- | ---: |
| [[arbitrary_symbol]] -> [[stable_attractor]] (can_settle_into) | 0.000000 |
| [[meaning]] -> [[stable_attractor]] (seeks) | 0.000000 |
| [[comfort]] -> [[stable_attractor]] (stabilizes) | 0.000000 |
