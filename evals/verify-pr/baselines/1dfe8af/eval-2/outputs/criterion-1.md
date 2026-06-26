# Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Result: FAIL

## Evidence

The filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs` is inverted. The code constructs:

```rust
let severity_order = ["critical", "high", "medium", "low"];
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

For `threshold=high`, the index into `severity_order` is 1. The conditions evaluate as:

- `critical`: always included (no condition). Correct.
- `high`: `threshold_idx <= 1` => `1 <= 1` => true, included. Correct.
- `medium`: `threshold_idx <= 2` => `1 <= 2` => true, included. **WRONG** -- medium should be excluded when threshold is high.
- `low`: `threshold_idx <= 3` => `1 <= 3` => true, included. **WRONG** -- low should be excluded when threshold is high.

The condition is backwards. It should be `threshold_idx >= N` (e.g., `threshold_idx >= 1` for high, `threshold_idx >= 2` for medium, `threshold_idx >= 3` for low) so that a higher threshold index (further down the severity list) includes more severities.

With `threshold=high`, the code returns all four severity counts instead of only critical and high. The criterion requires that only critical and high are returned, so this is a clear FAIL.

Additionally, the `total` field is computed from the unfiltered counts (`summary.critical + summary.high + summary.medium + summary.low`) rather than from the filtered values, which would produce an incorrect total even if the filter conditions were fixed.
