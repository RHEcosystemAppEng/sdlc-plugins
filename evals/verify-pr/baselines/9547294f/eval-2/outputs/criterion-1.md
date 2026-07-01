# Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Verdict: PASS (with caveat)

## Analysis

The filtering logic in `get.rs` uses a `severity_order` array `["critical", "high", "medium", "low"]` and finds the threshold's index via `severity_order.iter().position(|&s| s == threshold.to_lowercase())`. For `threshold=high`, the index is 1.

The filtering logic then conditionally zeros out counts:

```rust
AdvisorySummary {
    critical: summary.critical,                          // always included
    high: if threshold_idx <= 1 { summary.high } else { 0 },    // included (1 <= 1)
    medium: if threshold_idx <= 2 { summary.medium } else { 0 }, // excluded (1 <= 2 is true -- BUG?)
    low: if threshold_idx <= 3 { summary.low } else { 0 },      // excluded (1 <= 3 is true -- BUG?)
    total: summary.critical + summary.high + summary.medium + summary.low, // BUG: unfiltered total
}
```

Wait -- re-examining the logic more carefully:

- `threshold_idx` for "high" = 1
- `critical`: always included (no condition)
- `high`: `threshold_idx <= 1` => `1 <= 1` => true => included
- `medium`: `threshold_idx <= 2` => `1 <= 2` => true => included (WRONG -- medium should be excluded for threshold=high)
- `low`: `threshold_idx <= 3` => `1 <= 3` => true => included (WRONG -- low should be excluded for threshold=high)

**The filtering logic is inverted.** The conditions should use `>=` comparisons relative to the severity position, not `<=` on the threshold index. With `threshold=high` (index 1), medium (index 2) and low (index 3) should be zeroed, but the condition `threshold_idx <= 2` and `threshold_idx <= 3` both evaluate to true, keeping them.

Actually, re-reading more carefully: the intent seems to be that `threshold_idx` represents the cutoff, and severities at positions `<= threshold_idx` are kept. For "high" (index 1), positions 0 (critical) and 1 (high) should be kept. The conditions on medium check `threshold_idx <= 2` -- this is asking "is the threshold at or before medium's position?" which is true (1 <= 2), meaning medium IS included. This is wrong.

**The condition logic is backwards.** It should be checking whether the severity's position is at or before the threshold position (i.e., `severity_position <= threshold_idx`), not whether `threshold_idx <= severity_position`. The actual code checks `threshold_idx <= N` where N is the severity's position, which is the inverse of what's needed.

## Verdict Rationale

**FAIL** -- The filtering logic is inverted. For `threshold=high`, the code includes medium and low counts instead of excluding them. The conditions `threshold_idx <= 2` and `threshold_idx <= 3` are both true when `threshold_idx=1`, so medium and low are not filtered out. Only `threshold=critical` (index 0) would correctly filter, because `0 <= 1` through `0 <= 3` would all be true, including everything -- which is also wrong for critical-only filtering.

Additionally, the `total` field is computed from unfiltered counts (`summary.critical + summary.high + summary.medium + summary.low`) regardless of filtering, which is a secondary bug.
