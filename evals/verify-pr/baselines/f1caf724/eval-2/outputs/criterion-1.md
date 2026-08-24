# Criterion 1 Analysis

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

**Verdict:** FAIL

## Reasoning

The PR adds threshold filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs`, but the filtering comparison is inverted, causing incorrect results.

### Code Under Review

```rust
let filtered = match &params.threshold {
    Some(threshold) => {
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
    }
    None => summary,
};
```

### Bug 1: Inverted comparison logic

The severity_order array assigns indices: critical=0, high=1, medium=2, low=3 (highest to lowest severity). The requirement says "at or above the threshold," meaning only severities with index <= threshold_idx should be included.

However, the code checks `threshold_idx <= N` (where N is each severity's hardcoded position), which is the inverse condition. For `threshold=high` (threshold_idx=1):

- critical: always included (correct)
- high: `1 <= 1` is true, so high is included (correct by coincidence)
- medium: `1 <= 2` is true, so medium is INCLUDED (should be 0)
- low: `1 <= 3` is true, so low is INCLUDED (should be 0)

The correct comparison would be `N <= threshold_idx` (i.e., the severity's position must be at or before the threshold position). This means the filter includes severities at or BELOW the threshold instead of at or ABOVE it.

### Bug 2: Total computed from unfiltered counts

```rust
total: summary.critical + summary.high + summary.medium + summary.low,
```

The `total` field sums all original unfiltered severity counts, not the filtered ones. Even if the filtering logic were correct, the total would still be wrong because it does not reflect the filtered result. It should sum only the included (non-zeroed) values.

### Impact

With `threshold=high`, the endpoint returns all four severity counts instead of just critical and high. The filtering is functionally broken for all threshold values except "low" (which includes everything, same as no threshold).
