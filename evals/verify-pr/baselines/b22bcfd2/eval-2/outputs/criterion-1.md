# Criterion 1: Threshold filtering returns only at-or-above counts

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only.

**Verdict:** PASS (partial -- see caveats below)

## Analysis

The PR diff in `modules/fundamental/src/advisory/endpoints/get.rs` implements threshold filtering logic starting at the `let filtered = match &params.threshold` block (lines 41-56 of the diff).

The implementation defines a severity ordering array:

```rust
let severity_order = ["critical", "high", "medium", "low"];
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

For `threshold=high`, `position` returns `Some(1)`, so `threshold_idx = 1`. The filtering logic then evaluates:

- `critical`: always included (unconditionally set to `summary.critical`) -- correct
- `high`: `if threshold_idx <= 1` -- 1 <= 1 is true, so `summary.high` is included -- correct
- `medium`: `if threshold_idx <= 2` -- 1 <= 2 is true, so `summary.medium` is included -- **INCORRECT**
- `low`: `if threshold_idx <= 3` -- 1 <= 3 is true, so `summary.low` is included -- **INCORRECT**

**Wait -- re-examining the logic more carefully:** The condition checks `threshold_idx <= N` where N is the position of each severity level. For `threshold=high` (idx=1):
- critical (position 0): always included -- correct
- high (position 1): `1 <= 1` = true, included -- correct
- medium (position 2): `1 <= 2` = true, included -- **This is wrong!**
- low (position 3): `1 <= 3` = true, included -- **This is also wrong!**

Actually, the logic is inverted. The condition should be checking whether each severity's position is at or above the threshold (i.e., position <= threshold_idx), not whether the threshold_idx <= position. But looking at the code again:

```rust
high: if threshold_idx <= 1 { summary.high } else { 0 },
medium: if threshold_idx <= 2 { summary.medium } else { 0 },
low: if threshold_idx <= 3 { summary.low } else { 0 },
```

For `threshold=high` (threshold_idx = 1):
- `high`: threshold_idx (1) <= 1 -> true -> included
- `medium`: threshold_idx (1) <= 2 -> true -> included
- `low`: threshold_idx (1) <= 3 -> true -> included

This means `threshold=high` would include medium and low as well, which violates the criterion. Only critical and high should be returned.

**However**, there is a secondary issue: the `unwrap_or(0)` fallback. If an invalid threshold is passed, `position` returns `None` and `unwrap_or(0)` maps it to index 0 (critical). This means invalid thresholds silently behave like `threshold=critical` instead of returning 400.

**Re-examination:** Actually, let me reconsider whether the logic is correct for `threshold=high`. The severity_order is `["critical", "high", "medium", "low"]` with indices 0, 1, 2, 3. The intent is to include severities at or above the threshold. "Above" in severity means lower index (critical=0 is highest). So for `threshold=high` (idx=1), we want indices 0 and 1 (critical and high).

The correct condition for including a severity at position P would be: `P <= threshold_idx`. But the code checks `threshold_idx <= P`:
- For high (P=1): 1 <= 1 = true -- correct
- For medium (P=2): 1 <= 2 = true -- **wrong, should be excluded**
- For low (P=3): 1 <= 3 = true -- **wrong, should be excluded**

The condition is backwards. It should be `threshold_idx >= P` (or equivalently `P <= threshold_idx`) to filter properly. As written, `threshold=high` includes all four severities, which fails the criterion.

**Revised Verdict:** FAIL

The filtering logic has an inverted comparison. With `threshold=high`, medium and low counts are still included because `threshold_idx <= 2` and `threshold_idx <= 3` are both true when threshold_idx=1. The correct comparison should check whether each severity's position is within the threshold window (position <= threshold_idx), not whether the threshold index is less than the severity position.

Additionally, the `total` field is recomputed from all unfiltered counts (`summary.critical + summary.high + summary.medium + summary.low`) regardless of filtering, which means the total would not reflect the filtered subset even if the per-severity filtering were correct.
