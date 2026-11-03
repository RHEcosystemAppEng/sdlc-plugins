# Criterion 4: Severity ordering is correct: critical > high > medium > low

**Verdict: NOT MET (FAIL)**

## Reasoning

The array `["critical", "high", "medium", "low"]` lists the severities in the right order, but the filter compares against it backwards:

```rust
high: if threshold_idx <= 1 { summary.high } else { 0 },
medium: if threshold_idx <= 2 { summary.medium } else { 0 },
low: if threshold_idx <= 3 { summary.low } else { 0 },
```

"At or above the threshold" means keeping a severity at index `i` when `i <= threshold_idx`. The code checks `threshold_idx <= i`. Results for each valid threshold (critical is always kept):

| threshold | idx | high kept? | medium kept? | low kept? | Expected result | Actual result |
|---|---|---|---|---|---|---|
| critical | 0 | yes (0<=1) | yes (0<=2) | yes (0<=3) | critical | critical, high, medium, low |
| high | 1 | yes (1<=1) | yes (1<=2) | yes (1<=3) | critical, high | critical, high, medium, low |
| medium | 2 | no (2<=1) | yes (2<=2) | yes (2<=3) | critical, high, medium | critical, medium, low |
| low | 3 | no | no | yes (3<=3) | all four | critical, low |

All four thresholds give the wrong result. The code keeps severities *below* the threshold and drops the ones above it, with critical always kept as a special case. The effective ordering is not critical > high > medium > low.

The Implementation Notes ask for a `Severity` enum (`Critical`, `High`, `Medium`, `Low`) that implements `Ord`. The PR does not define one. It uses hardcoded string positions and hand-written index checks, and the inversion comes from those checks.

## Test coverage
None. The required tests for threshold=critical, threshold=high and threshold=medium do not exist. Each would fail against this implementation.
