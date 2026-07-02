# Acceptance Criterion 1

**Criterion**: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

**Result**: FAIL

## Evidence

The filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs` does attempt to filter severities based on the threshold index:

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

For `threshold=high`, `threshold_idx` would be 1, so `critical` and `high` are included while `medium` and `low` are zeroed out. The filtering logic for individual severity counts is correct for this case.

However, the `total` field is computed from the **unfiltered** counts (`summary.critical + summary.high + summary.medium + summary.low`) rather than the filtered counts. When `threshold=high`, `total` should equal `critical + high`, but instead it equals the sum of all four unfiltered severities. This means the response is internally inconsistent -- the individual severity counts are filtered but `total` is not.

**Verdict**: FAIL -- the `total` field does not reflect the filtered counts, making the response incorrect.
