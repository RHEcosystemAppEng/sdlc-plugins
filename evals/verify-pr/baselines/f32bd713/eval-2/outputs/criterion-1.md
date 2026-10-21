# Criterion 1: threshold=high returns counts for critical and high only

## Verdict: FAIL

## Criterion Text
`GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Analysis

The filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs` is implemented with an inverted comparison. The code uses `threshold_idx <= N` where it should use `N <= threshold_idx` (i.e., severity position <= threshold index).

### Code Under Review

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

### Trace for threshold=high

- `threshold_idx` = 1 (position of "high" in `severity_order`)
- `critical`: always kept (unconditional) -- correct
- `high`: `threshold_idx(1) <= 1` = true -- kept (correct)
- `medium`: `threshold_idx(1) <= 2` = true -- kept (INCORRECT, should be 0)
- `low`: `threshold_idx(1) <= 3` = true -- kept (INCORRECT, should be 0)

The condition `threshold_idx <= severity_position` means "include this severity if the threshold is at or above this level." For threshold=high (idx=1), all severities with position >= 1 are included, which is medium and low -- the opposite of the intended behavior.

The correct condition would be `severity_position <= threshold_idx`: include a severity if its rank (position in the array, where 0=critical is highest) is at most the threshold's rank. For threshold=high (idx=1): critical(0<=1=true), high(1<=1=true), medium(2<=1=false), low(3<=1=false).

### Additional Issue: Incorrect Total

The `total` field is computed from unfiltered values:
```rust
total: summary.critical + summary.high + summary.medium + summary.low,
```
This sums the original (unfiltered) counts rather than the filtered counts, so even if the filtering were correct, the total would be wrong.

## Evidence
- File: `modules/fundamental/src/advisory/endpoints/get.rs`, lines 41-55
- The comparison `threshold_idx <= N` is inverted; should be `N <= threshold_idx`
- For threshold=high, the endpoint returns all four severity counts instead of only critical and high
- Total is always the sum of unfiltered counts
