# Criterion 1

**Criterion**: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Analysis

The filtering logic is implemented in `modules/fundamental/src/advisory/endpoints/get.rs`. When `threshold=high` is provided, the code performs the following:

1. Looks up `"high"` in `severity_order = ["critical", "high", "medium", "low"]`, finding `threshold_idx = 1`.
2. Applies conditions per severity field:
   - `critical: summary.critical` — always included (correct)
   - `high: if threshold_idx <= 1` — evaluates `1 <= 1` = true — included (correct)
   - `medium: if threshold_idx <= 2` — evaluates `1 <= 2` = true — **included (BUG)**
   - `low: if threshold_idx <= 3` — evaluates `1 <= 3` = true — **included (BUG)**

The comparison is inverted. The code checks `threshold_idx <= severity_position` when it should check `severity_position <= threshold_idx`. With `threshold=high`, all four severity levels are included in the response instead of just critical and high.

The correct conditions should be:
- `high: if 1 <= threshold_idx` (include high when threshold is high, medium, or low)
- `medium: if 2 <= threshold_idx` (include medium when threshold is medium or low)
- `low: if 3 <= threshold_idx` (include low only when threshold is low)

Additionally, the `total` field is computed as `summary.critical + summary.high + summary.medium + summary.low` using the **unfiltered** counts, so even if filtering were correct, the total would not reflect the filtered results.

## Verdict: FAIL

The filtering logic has an inverted comparison that causes all severity levels to be returned regardless of the threshold value. The `total` field also uses unfiltered counts.
