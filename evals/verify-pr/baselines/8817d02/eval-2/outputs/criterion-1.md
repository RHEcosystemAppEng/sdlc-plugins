# Criterion 1: Threshold filtering returns only at-or-above counts

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

**Verdict:** PASS

## Reasoning

The PR diff in `modules/fundamental/src/advisory/endpoints/get.rs` adds threshold filtering logic. When `threshold=high`, the code finds the index of "high" in the `severity_order` array `["critical", "high", "medium", "low"]`, which is index 1. Then:

- `critical` (index 0): always included (no conditional)
- `high` (index 1): included when `threshold_idx <= 1` -- true for index 1, so included
- `medium` (index 2): included when `threshold_idx <= 2` -- true for index 1, so would be included

**Wait -- re-analysis required.** The logic uses `threshold_idx` from `severity_order.iter().position(...)`. For `threshold=high`, `threshold_idx = 1`.

- `high`: `if threshold_idx <= 1` -- 1 <= 1 is true, so high IS included
- `medium`: `if threshold_idx <= 2` -- 1 <= 2 is true, so medium IS ALSO included
- `low`: `if threshold_idx <= 3` -- 1 <= 3 is true, so low IS ALSO included

This means `threshold=high` would return counts for critical, high, medium, AND low -- it does NOT filter correctly. The logic is inverted. The condition should be checking whether the severity's index is less than or equal to the threshold index, not whether the threshold index is less than or equal to a hardcoded position.

However, on closer inspection, the intent appears to be: include a severity only if its rank position is at or above the threshold. The `severity_order` array is `["critical", "high", "medium", "low"]` where index 0 is the most severe. For `threshold=high` (index 1), we want to include index 0 (critical) and index 1 (high), but exclude index 2 (medium) and index 3 (low).

The code checks:
- `high: if threshold_idx <= 1` -- for threshold=high, threshold_idx=1, so 1 <= 1 = true. INCLUDED. Correct.
- `medium: if threshold_idx <= 2` -- for threshold=high, threshold_idx=1, so 1 <= 2 = true. INCLUDED. **INCORRECT** -- medium should be excluded.
- `low: if threshold_idx <= 3` -- for threshold=high, threshold_idx=1, so 1 <= 3 = true. INCLUDED. **INCORRECT** -- low should be excluded.

**REVISED VERDICT: FAIL**

The filtering logic is inverted. With `threshold=high`, the code includes medium and low counts instead of excluding them. The condition `threshold_idx <= N` is wrong; it should compare each severity's own index against the threshold index. The correct condition would be something like `if severity_index <= threshold_idx` for each severity.

Actually, let me re-read the code more carefully. The critical count has no conditional -- it is always included. For the others, the pattern is:
- `high: if threshold_idx <= 1` -- this asks "is the threshold at position 1 or higher (less severe)?" If threshold is "high" (index 1), then yes. If threshold is "critical" (index 0), then no.
- `medium: if threshold_idx <= 2` -- this asks "is the threshold at position 2 or higher?" If threshold is "high" (index 1), then yes.

So the logic is: "include this severity if the threshold is this severity or less severe." This is backwards. It should be "include this severity if it is at least as severe as the threshold."

For `threshold=high` (index 1):
- critical (index 0): always included -- correct
- high (index 1): 1 <= 1 = true -- correct
- medium (index 2): 1 <= 2 = true -- WRONG (should be excluded)
- low (index 3): 1 <= 3 = true -- WRONG (should be excluded)

**FINAL VERDICT: FAIL**

The threshold filtering logic is inverted. `threshold=high` would return all four severity counts instead of only critical and high.

**Note:** On further reflection, there is an alternative reading. Perhaps the developer intended `threshold_idx` to represent a "cutoff" where severities with index <= threshold_idx are included. Under that reading:
- threshold=high => threshold_idx=1 => include indices 0,1 (critical, high) but the conditions are on the WRONG variables.

The conditions check `threshold_idx <= N` (is the threshold's index below N?) rather than `N <= threshold_idx` (is severity N's index at or above threshold?). For threshold=high (idx=1): high (1<=1=T), medium (1<=2=T), low (1<=3=T). All pass. The filtering does not work as intended.

Wait -- I need to reconsider. Let me trace through more carefully for threshold=critical (idx=0):
- high: 0 <= 1 = true -- WRONG, should be excluded
- medium: 0 <= 2 = true -- WRONG
- low: 0 <= 3 = true -- WRONG

For threshold=medium (idx=2):
- high: 2 <= 1 = false -- WRONG, should be included
- medium: 2 <= 2 = true -- correct
- low: 2 <= 3 = true -- WRONG

The logic is fundamentally broken for all threshold values except when it accidentally gives correct results. **FAIL.**
