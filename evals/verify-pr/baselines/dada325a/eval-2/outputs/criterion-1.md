# Criterion 1 — FAIL

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## What was checked

The new `match &params.threshold` block in `modules/fundamental/src/advisory/endpoints/get.rs`. No filtering was added to `advisory.rs`. That hunk has context lines only, with no `+`/`-` lines.

## Findings

```rust
let severity_order = ["critical", "high", "medium", "low"];
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
AdvisorySummary {
    critical: summary.critical,
    high:   if threshold_idx <= 1 { summary.high }   else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low:    if threshold_idx <= 3 { summary.low }    else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

1. **The comparison is the wrong way round.** With `threshold=high`, `threshold_idx = 1`:
   - high: `1 <= 1` is true, so it is included (correct)
   - medium: `1 <= 2` is true, so it is **included** (wrong, it should be 0)
   - low: `1 <= 3` is true, so it is **included** (wrong, it should be 0)

   So `?threshold=high` returns all four counts and filters nothing. The other values are also wrong:
   - `threshold=critical` (idx 0) returns all four counts.
   - `threshold=low` (idx 3) returns only critical and low.

   The check should be `threshold_idx >= N`, not `<= N`.
2. **`total` uses the unfiltered counts.** Even if the comparison were fixed, `total` adds up the original `summary.*` values rather than the filtered ones, so it would include medium and low.
3. Severities below the threshold are set to `0` rather than left out. The task says "omitting `medium` and `low`". Zeroing them could be accepted with a note, but it does not match the description exactly.

## Verdict

FAIL. The endpoint does not return only the critical and high counts for `threshold=high`. No test covers this case (`tests/api/advisory_summary.rs` was not created).
