# Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

**Verdict: FAIL**

## Reasoning

The handler in `modules/fundamental/src/advisory/endpoints/get.rs` zeroes the per-severity counts below the threshold:

```rust
high: if threshold_idx <= 1 { summary.high } else { 0 },
medium: if threshold_idx <= 2 { summary.medium } else { 0 },
low: if threshold_idx <= 3 { summary.low } else { 0 },
total: summary.critical + summary.high + summary.medium + summary.low,
```

For `threshold=high`, `threshold_idx` is 1, so `medium` and `low` come back as `0`. The individual severity masking is correct. The criterion still fails for two reasons:

1. **`total` comes from the unfiltered counts.** It adds `summary.medium` and `summary.low` from the original aggregate, not from the filtered values. Example: with critical=2, high=3, medium=5, low=7, the response is `{critical: 2, high: 3, medium: 0, low: 0, total: 17}`. The correct total is 5. The response therefore still carries medium and low data, and it contradicts itself.
2. **Medium and low are not omitted.** They are returned as `0`. The task Description says `?threshold=high` "returns counts for `critical` and `high` only, omitting `medium` and `low`". A `0` value cannot be told apart from a real zero count.

The task also asked for the filter to be applied in the aggregation query in `advisory.rs`, through an optional WHERE clause on severity rank. The diff's `advisory.rs` hunk has only context lines and makes no change. Filtering happens after aggregation, in the handler.

No test was added to cover this case. The required `tests/api/advisory_summary.rs` is absent.

## Evidence
- `get.rs`: the filtered `AdvisorySummary` literal (the `total:` line uses the unfiltered `summary.*` fields)
- `advisory.rs` hunk `@@ -45,6 +45,7 @@`: no `+` or `-` lines
