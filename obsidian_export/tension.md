# Tension

## Node

- Node id: `tension`
- Activation: 0.000000
- Stability: 1.000000

## Metadata

```yaml
type: state
```

## Outgoing Edges

_None._

## Incoming Edges

- [[religion]]: can_raise (weight=0.050, polarity=1.000)
- [[trauma]]: increases (weight=0.100, polarity=1.000)
- [[control]]: increases (weight=0.850, polarity=1.000)
- [[comfort]]: relaxes (weight=0.800, polarity=-1.000)

## Current Tension Contributions

Outgoing:

_None._

Incoming:

| Edge | Tension |
| --- | ---: |
| [[religion]] -> [[tension]] (can_raise) | 0.000000 |
| [[trauma]] -> [[tension]] (increases) | 0.000000 |
| [[control]] -> [[tension]] (increases) | 0.000000 |
| [[comfort]] -> [[tension]] (relaxes) | 0.000000 |
