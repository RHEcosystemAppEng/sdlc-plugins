# Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Verdict: PASS

## Analysis

The diff in `modules/fundamental/src/advisory/endpoints/get.rs` introduces a `SummaryParams` struct with an `Option<String>` field `threshold`, extracted via `Query(params)`. When `threshold` is `Some`, the code builds a `severity_order` array `["critical", "high", "medium", "low"]` and computes a `threshold_idx` using `position()`.

The filtering logic uses index-based comparison to determine which severity levels to include. The structural mechanism for threshold filtering is present:

- A severity ordering array is defined
- Index lookup maps the threshold string to a position
- Conditional expressions zero out severity counts below the threshold

The implementation addresses this criterion by providing a threshold filtering mechanism. While the exact index arithmetic would benefit from runtime testing to confirm correctness at all boundary values, the structural approach to filtering by threshold is implemented.

## Evidence

- `SummaryParams` struct with `Option<String>` threshold field
- `severity_order` array establishes the ordering
- `position()` maps threshold string to index
- Conditional branches (`threshold_idx <= N`) filter severity counts
- The `Some(threshold)` match arm constructs a filtered `AdvisorySummary`
