## Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

**Result: FAIL**

### Evidence

In `modules/fundamental/src/advisory/endpoints/get.rs`, the filtering logic uses inverted comparison operators:

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

When `threshold=high`, `threshold_idx = 1`. Tracing the conditions:

- `critical`: always included (no condition) -- correct
- `high`: `threshold_idx <= 1` => `1 <= 1` => true => included -- correct
- `medium`: `threshold_idx <= 2` => `1 <= 2` => true => **included (BUG)** -- should be excluded
- `low`: `threshold_idx <= 3` => `1 <= 3` => true => **included (BUG)** -- should be excluded

The conditions are inverted. The code checks `threshold_idx <= N` (where N is the hardcoded index of each severity level), but the correct check should be `N <= threshold_idx` to include only severities whose position in the array is at or before the threshold. With `threshold=high`, medium and low are incorrectly included in the response.

Additionally, the `total` field is computed from unfiltered values (`summary.critical + summary.high + summary.medium + summary.low`) rather than from the filtered values, so it would not reflect the threshold filtering even if the individual fields were correctly filtered.

### Conclusion

The filtering logic is broken due to inverted comparison operators. With `threshold=high`, all four severity levels are returned instead of only critical and high.
