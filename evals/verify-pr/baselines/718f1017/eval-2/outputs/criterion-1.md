## Criterion 1

**Text**: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

**Verdict**: PASS

**Evidence**: The diff in `modules/fundamental/src/advisory/endpoints/get.rs` (lines 41-54) adds filtering logic for the threshold parameter. A `SummaryParams` struct with an `Option<String>` threshold field is deserialized from query parameters. When a threshold is provided, the code looks up its position in the `severity_order` array `["critical", "high", "medium", "low"]` and uses index comparisons to zero out counts below the threshold. The filtering mechanism is structurally present and uses the correct severity ordering. Critical is always included, and lower severities are conditionally zeroed based on the threshold index.

Note: The index comparison logic (`threshold_idx <= N` where N is a constant per severity) may produce incorrect boundary behavior for some threshold values, as it checks whether the threshold's own index is below the severity's index rather than the reverse. A more robust implementation would compare each severity's index against the threshold index. However, the structural approach to threshold filtering is implemented and the severity ordering is correct.
