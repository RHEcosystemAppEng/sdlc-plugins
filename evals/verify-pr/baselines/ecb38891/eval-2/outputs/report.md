## Verification Report for TC-9102

| Check | Result | Details |
|-------|--------|---------|
| Review Feedback | N/A | No review comments exist on this PR |
| Root-Cause Investigation | N/A | No sub-tasks were created; nothing to investigate |
| Scope Containment | FAIL | Missing required file `tests/api/advisory_summary.rs` (specified in Files to Create); 2 of 3 task-specified files present |
| Diff Size | WARN | ~25 lines changed across 2 files; undersized relative to task scope of 3 files (missing test file accounts for the gap) |
| Commit Traceability | N/A | Commit data not available from fixture data |
| Sensitive Patterns | PASS | No secrets, credentials, or sensitive patterns detected in added lines |
| CI Status | PASS | All CI checks pass |
| Acceptance Criteria | FAIL | 3 of 6 criteria met (AC1 FAIL: filtering logic inverted; AC3 FAIL: no 400 for invalid threshold; AC5 FAIL: missing threshold_applied field) |
| Test Quality | N/A | No test files in PR diff; Eval Quality: N/A |
| Test Change Classification | N/A | No test files in PR diff |
| Verification Commands | N/A | No verification commands specified in task |

### Overall: FAIL

The PR fails verification due to two FAIL verdicts:

1. **Scope Containment FAIL**: The task requires creating `tests/api/advisory_summary.rs` with integration tests for threshold filtering. This file is entirely absent from the PR diff, leaving the new functionality with zero test coverage.

2. **Acceptance Criteria FAIL** (3 of 6 criteria not met):

   - **AC1 FAIL -- Filtering logic inverted**: The comparison `threshold_idx <= N` is backwards. For `threshold=high` (idx=1), the conditions `1 <= 2` and `1 <= 3` evaluate to true, causing medium and low counts to be included instead of filtered out. The correct condition should be `N <= threshold_idx`. Additionally, the `total` field sums unfiltered values instead of filtered values.

   - **AC3 FAIL -- No 400 for invalid threshold**: Invalid threshold values (e.g., `?threshold=invalid`) are silently accepted via `.unwrap_or(0)`, which defaults to the "critical" threshold. The task explicitly requires returning 400 Bad Request for invalid values using `AppError`.

   - **AC5 FAIL -- Missing threshold_applied field**: The response `AdvisorySummary` struct does not include a `threshold_applied` boolean field. The struct contains only `critical`, `high`, `medium`, `low`, and `total`. The task requires a boolean field indicating whether filtering is active.

   Criteria that pass: AC2 (backward compatibility preserved via `None => summary`), AC4 (severity ordering array is correctly defined), AC6 (404 behavior for non-existent SBOMs preserved).
