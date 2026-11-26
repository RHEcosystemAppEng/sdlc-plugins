# Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

**Verdict: NOT MET**

## Reasoning
With `threshold=high`, the handler in `modules/fundamental/src/advisory/endpoints/get.rs` computes `threshold_idx = 1` from the string array `["critical", "high", "medium", "low"]`. `critical` and `high` keep their real values. `medium` and `low` are set to `0`. This falls short of the criterion in two ways:

1. **Below-threshold severities are zeroed, not omitted.** The task description says `?threshold=high` "returns counts for `critical` and `high` only, omitting `medium` and `low`". The response still contains `medium: 0` and `low: 0`, and a client cannot tell these apart from "this SBOM has no medium/low advisories".
2. **`total` is computed from the unfiltered counts.** The total field is `summary.critical + summary.high + summary.medium + summary.low`, which uses the original aggregate values. Example: an SBOM with critical=1, high=2, medium=3, low=4 queried with `?threshold=high` returns `{critical:1, high:2, medium:0, low:0, total:10}`. The total should be 3, and the response contradicts itself.

The task's implementation notes also asked for the filter to go into the aggregation query in `advisory.rs` as a WHERE on severity rank. The `advisory.rs` hunk contains no added or removed lines. The filtering is done after aggregation, in the handler.

## Evidence
- `get.rs` (added): `high: if threshold_idx <= 1 { summary.high } else { 0 },`
- `get.rs` (added): `medium: if threshold_idx <= 2 { summary.medium } else { 0 },`
- `get.rs` (added): `low: if threshold_idx <= 3 { summary.low } else { 0 },`
- `get.rs` (added): `total: summary.critical + summary.high + summary.medium + summary.low,`
- `advisory.rs` hunk `@@ -45,6 +45,7 @@` contains context lines only.
- No test for threshold=high: `tests/api/advisory_summary.rs` was not created.
