# Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

**Verdict: NOT MET (FAIL)**

## Evidence (modules/fundamental/src/advisory/endpoints/get.rs)

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

## Reasoning

- `threshold=high` gives `threshold_idx = 1`.
- `high`: `1 <= 1` is true, so it is kept.
- `medium`: `1 <= 2` is true, so it is **kept**. It should be omitted.
- `low`: `1 <= 3` is true, so it is **kept**. It should be omitted.
- So `?threshold=high` returns all four counts, the same as no filter.

The comparisons are inverted. A severity at index `i` should be kept when `i <= threshold_idx`, but the code keeps it when `threshold_idx <= i`.

Two more problems:
- `total` always sums the **unfiltered** counts, so it never matches the filtered values.
- The design zeroes excluded severities instead of omitting them. That is ambiguous: a filtered-out 0 looks the same as a real 0.

The filtering is also done in the handler rather than as a WHERE clause in the aggregation query in `advisory.rs`, which the Implementation Notes asked for. The `advisory.rs` hunk has no actual added or removed lines.

No test covers this case: `tests/api/advisory_summary.rs` was not created.
