## Verification Report for TC-9102

| Check | Result | Details |
|-------|--------|---------|
| Review Feedback | N/A | No review comments |
| Root-Cause Investigation | N/A | No sub-tasks created |
| Scope Containment | FAIL | `tests/api/advisory_summary.rs` is listed in Files to Create but is entirely absent from the diff. Both files to modify (`get.rs`, `advisory.rs`) are present, but the required test file was never created. |
| Diff Size | PASS | ~30 lines added across 2 files; proportionate for adding a query parameter with filtering logic, though incomplete due to missing test file |
| Commit Traceability | PASS | Diff modifies the files specified in TC-9102 (advisory endpoints and service) |
| Sensitive Patterns | PASS | No secrets, credentials, API keys, or sensitive data found in added lines |
| CI Status | PASS | All CI checks pass |
| Acceptance Criteria | FAIL | 2 of 6 criteria met (see per-criterion files for detailed evidence) |
| Test Quality | N/A | No test files present in the diff |
| Test Change Classification | N/A | No test files exist in the PR diff |
| Verification Commands | N/A | No verification commands |

### Acceptance Criteria Summary

| # | Criterion | Result |
|---|-----------|--------|
| 1 | `threshold=high` returns counts for critical and high only | FAIL |
| 2 | Without threshold returns all severity counts (backward compatible) | PASS |
| 3 | `threshold=invalid` returns 400 Bad Request | FAIL |
| 4 | Severity ordering is correct: critical > high > medium > low | FAIL |
| 5 | Response includes `threshold_applied` boolean field | FAIL |
| 6 | Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved) | PASS |

### Detailed Findings

**Criterion 1 (FAIL):** The filtering logic in `get.rs` uses inverted conditions. The code checks `threshold_idx <= N` when it should check `threshold_idx >= N`. For `threshold=high` (idx=1), the conditions `1 <= 2` and `1 <= 3` evaluate to true, causing medium and low counts to be included when they should be zeroed out. Additionally, the `total` field is computed from unfiltered counts rather than filtered values.

**Criterion 3 (FAIL):** Invalid threshold values are silently accepted via `.unwrap_or(0)`, which maps unrecognized strings to index 0 (effectively treating them as `threshold=critical`). The task requires returning a 400 Bad Request error using the existing `AppError` pattern from `common/src/error.rs`. No validation or error response is implemented.

**Criterion 4 (FAIL):** While the severity ordering array `["critical", "high", "medium", "low"]` is correctly defined, the inverted filtering logic means the ordering is not correctly applied in practice. For example, `threshold=medium` excludes high but includes medium, which contradicts the ordering where high is above medium.

**Criterion 5 (FAIL):** The response `AdvisorySummary` struct contains only `critical`, `high`, `medium`, `low`, and `total` fields. The required `threshold_applied` boolean field is entirely absent from both the response construction and the model definition. No modification to the `AdvisorySummary` struct in `model/summary.rs` appears in the diff.

**Missing Test File:** The task specifies creating `tests/api/advisory_summary.rs` with 6 test cases. This file is completely absent from the PR diff, meaning none of the test requirements are satisfied.

### Overall: FAIL
