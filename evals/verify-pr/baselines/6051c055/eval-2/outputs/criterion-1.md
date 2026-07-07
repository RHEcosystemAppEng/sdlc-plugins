# Criterion 1 Analysis

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

**Verdict:** FAIL

## Analysis

The filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs` is incorrect. The code uses inverted comparison conditions that cause the filter to include severity levels that should be excluded.

### Code Under Test

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

### Trace for threshold="high"

- `severity_order` = `["critical", "high", "medium", "low"]`
- `threshold_idx` = 1 (position of "high")
- critical: always included (correct)
- high: `threshold_idx <= 1` => `1 <= 1` => true => included (correct)
- medium: `threshold_idx <= 2` => `1 <= 2` => true => **INCLUDED** (WRONG -- should be 0)
- low: `threshold_idx <= 3` => `1 <= 3` => true => **INCLUDED** (WRONG -- should be 0)

The code checks `threshold_idx <= field_constant` instead of the correct `field_index <= threshold_idx`. This inverts the filtering: lower-severity counts are included when they should be excluded.

For threshold=high, the response includes all four severity counts instead of only critical and high.

### Additional Bug

The `total` field is computed from unfiltered counts (`summary.critical + summary.high + summary.medium + summary.low`) rather than from the filtered counts, so even if the per-field filtering were correct, the total would not reflect the filtered result.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`, lines 31-44
- The conditions `threshold_idx <= 1`, `threshold_idx <= 2`, `threshold_idx <= 3` are inverted; the correct conditions would be `1 <= threshold_idx`, `2 <= threshold_idx`, `3 <= threshold_idx` (i.e., include a severity level only if its index is within the threshold range)
