# Trauma

## Node

- Node id: `trauma`
- Activation: 0.000000
- Stability: 1.000000

## Metadata

```yaml
type: memory
```

## Outgoing Edges

- increases: [[tension]] (weight=0.100, polarity=1.000)
- disrupts: [[comfort]] (weight=1.300, polarity=-1.000)
- disrupts: [[ritual]] (weight=1.000, polarity=-1.000)
- isolates: [[community]] (weight=1.000, polarity=-1.000)

## Incoming Edges

- [[religion]]: can_trigger (weight=0.050, polarity=1.000)

## Current Tension Contributions

Outgoing:

| Edge | Tension |
| --- | ---: |
| [[trauma]] -> [[tension]] (increases) | 0.000000 |
| [[trauma]] -> [[comfort]] (disrupts) | 0.000000 |
| [[trauma]] -> [[ritual]] (disrupts) | 0.000000 |
| [[trauma]] -> [[community]] (isolates) | 0.000000 |

Incoming:

| Edge | Tension |
| --- | ---: |
| [[religion]] -> [[trauma]] (can_trigger) | 0.000000 |
