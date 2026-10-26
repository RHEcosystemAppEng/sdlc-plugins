# Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Verdict: FAIL

## Reasoning

The filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs` contains an inverted comparison that renders the threshold filtering non-functional for this case.

The code defines `severity_order = ["critical", "high", "medium", "low"]` with indices 0, 1, 2, 3 respectively. For `threshold=high`, `threshold_idx` resolves to 1. The intent is to include only severities at or above high (i.e., critical and high).

However, the comparison is backwards. The code checks `threshold_idx <= constant` instead of `constant <= threshold_idx`:

```rust
high: if threshold_idx <= 1 { summary.high } else { 0 },    // 1 <= 1 -> true (correct by coincidence)
medium: if threshold_idx <= 2 { summary.medium } else { 0 }, // 1 <= 2 -> true (BUG: should be excluded)
low: if threshold_idx <= 3 { summary.low } else { 0 },       // 1 <= 3 -> true (BUG: should be excluded)
```

With `threshold=high`, medium and low are still included in the response. The correct condition should be `1 <= threshold_idx` (for high), `2 <= threshold_idx` (for medium), `3 <= threshold_idx` (for low) -- i.e., include a severity only if its rank index is at or below the threshold index.

Additionally, the `total` field is computed from unfiltered counts (`summary.critical + summary.high + summary.medium + summary.low`) rather than from the filtered values, so even if the individual counts were correctly filtered, the total would not match.
