# Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Verdict: FAIL

## Analysis

The diff adds threshold filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs`. The code defines `severity_order = ["critical", "high", "medium", "low"]` with indices 0, 1, 2, 3 respectively. For `threshold=high`, `threshold_idx = 1`.

The filtering conditionals check `threshold_idx <= N` for each severity level:
- `critical`: always included (no condition)
- `high`: included if `threshold_idx <= 1` -- with threshold_idx=1, evaluates to `1 <= 1` = true. High is included. Correct.
- `medium`: included if `threshold_idx <= 2` -- with threshold_idx=1, evaluates to `1 <= 2` = true. Medium is INCLUDED. **Incorrect** -- should be excluded for threshold=high.
- `low`: included if `threshold_idx <= 3` -- with threshold_idx=1, evaluates to `1 <= 3` = true. Low is INCLUDED. **Incorrect** -- should be excluded for threshold=high.

The comparison direction is inverted. The code checks `threshold_idx <= severity_position` when it should check `severity_position <= threshold_idx`. As a result, `threshold=high` returns all four severity counts instead of only critical and high.

Additionally, the `total` field is computed from the unfiltered values (`summary.critical + summary.high + summary.medium + summary.low`) rather than the filtered values, so even if the filtering were corrected, the total would be wrong.

## Conclusion

**FAIL** -- The filtering logic has a comparison direction bug that causes medium and low to be incorrectly included when threshold=high. The total is also computed from unfiltered values.
