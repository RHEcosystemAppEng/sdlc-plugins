# Criterion 1: threshold=high returns counts for critical and high only

## Criterion Text
`GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Verdict: FAIL

## Analysis

The filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs` is fundamentally broken. The code uses `unwrap_or(0)` to look up the threshold index in the severity_order array `["critical", "high", "medium", "low"]`, and then applies conditions using hardcoded index comparisons.

For `threshold=high`, `threshold_idx = 1`. The conditions are:

- `critical`: always included (no condition) -- correct
- `high`: `if threshold_idx <= 1` => `1 <= 1` => true -- happens to be correct by coincidence
- `medium`: `if threshold_idx <= 2` => `1 <= 2` => true -- **WRONG**, medium should be excluded
- `low`: `if threshold_idx <= 3` => `1 <= 3` => true -- **WRONG**, low should be excluded

The logic compares `threshold_idx <= hardcoded_severity_position` which is inverted. The correct comparison should be the severity's position index <= threshold_idx (i.e., include severities whose rank index is at or below the threshold index in the ordered array). As implemented, `threshold=high` would include all four severity levels instead of only critical and high.

## Evidence

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

The condition `threshold_idx <= N` is always true when threshold_idx is smaller than or equal to the hardcoded position, meaning nearly all severity levels are included regardless of the threshold. The correct approach would be something like `if N <= threshold_idx { ... }` where N is the severity's own index in the ordered array.
