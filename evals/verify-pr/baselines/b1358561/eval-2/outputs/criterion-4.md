# Criterion 4: Severity ordering is correct: critical > high > medium > low

**Verdict: NOT MET (FAIL)**

## Evidence (get.rs)

```rust
let severity_order = ["critical", "high", "medium", "low"];
...
high:   if threshold_idx <= 1 { summary.high }   else { 0 },
medium: if threshold_idx <= 2 { summary.medium } else { 0 },
low:    if threshold_idx <= 3 { summary.low }    else { 0 },
```

## Reasoning

The array lists severities in the right order, but the comparisons that use it are inverted. The table shows what each threshold actually returns.

| threshold | idx | critical | high | medium | low | expected |
|---|---|---|---|---|---|---|
| critical | 0 | kept | kept | kept | kept | critical only |
| high | 1 | kept | kept | kept | kept | critical + high |
| medium | 2 | kept | 0 | kept | kept | critical + high + medium |
| low | 3 | kept | 0 | 0 | kept | all four |

- `critical` and `low` are always kept.
- The middle severities are dropped exactly when they should be kept, so the ordering behaves backwards.
- The Implementation Notes asked for a `Severity` enum implementing `Ord` (`Critical`, `High`, `Medium`, `Low`). It was not defined; the code compares raw strings and array indices instead.
- None of the ordering tests (threshold=critical, high, medium) exist.
