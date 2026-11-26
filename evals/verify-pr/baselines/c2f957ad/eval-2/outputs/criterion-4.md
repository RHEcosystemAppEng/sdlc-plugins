# Criterion 4: Severity ordering is correct: critical > high > medium > low

**Verdict: PASS (with caveats)**

## Evidence (modules/fundamental/src/advisory/endpoints/get.rs)

```rust
let severity_order = ["critical", "high", "medium", "low"];
...
critical: summary.critical,
high: if threshold_idx <= 1 { summary.high } else { 0 },
medium: if threshold_idx <= 2 { summary.medium } else { 0 },
low: if threshold_idx <= 3 { summary.low } else { 0 },
```

## Reasoning

- The array order and the `<=` index checks give the right inclusion behavior:
  - `critical` (0): critical only
  - `high` (1): critical and high
  - `medium` (2): critical, high, and medium
  - `low` (3): all four
- Critical is always included, which fits it being the highest severity. Matching is case-insensitive via `to_lowercase()`.
- Caveats (these do not change the verdict on ordering itself):
  - The Implementation Notes asked for a `Severity` enum with `Critical`, `High`, `Medium`, `Low` variants implementing `Ord`. That was not done. The ordering is an ad-hoc string array inside the handler, so it cannot be reused or type-checked.
  - Invalid values fall back to the `critical` position instead of being rejected (see Criterion 3).
  - No test checks the ordering. The threshold=critical/high/medium tests are missing.

The ordering semantics are correct, so the criterion is met. The implementation does not follow the prescribed approach.
