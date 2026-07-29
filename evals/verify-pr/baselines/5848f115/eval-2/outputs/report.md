## Verification Report for TC-9102

| Check | Result | Details |
|-------|--------|---------|
| Review Feedback | N/A | No review comments on this PR |
| Root-Cause Investigation | N/A | No sub-tasks created; nothing to investigate |
| Scope Containment | FAIL | Required test file `tests/api/advisory_summary.rs` not created; task specifies 3 files (2 modify, 1 create) but only 2 files modified |
| Diff Size | WARN | ~26 lines added across 2 files; missing entire test file and substantive service-layer logic; diff is undersized relative to task scope |
| Commit Traceability | N/A | Commit messages not available in eval context |
| Sensitive Patterns | PASS | No secrets, credentials, or sensitive patterns detected in added lines |
| CI Status | PASS | All CI checks pass |
| Acceptance Criteria | FAIL | 2 of 6 criteria met; filtering logic has inverted conditions, no 400 on invalid input, missing `threshold_applied` field, total uses unfiltered counts |
| Test Quality | N/A | No test files in PR diff; Eval Quality: N/A |
| Test Change Classification | N/A | No test files in PR diff |
| Verification Commands | N/A | No verification commands specified in task |

### Overall: FAIL

#### Summary of Issues

**Critical -- Acceptance Criteria failures (4 of 6 criteria not met):**

1. **Filtering logic bug (Criteria 1, 4):** The threshold filtering conditions in `modules/fundamental/src/advisory/endpoints/get.rs` are inverted. The code checks `threshold_idx <= severity_constant` when it should check `severity_constant <= threshold_idx`. This causes incorrect filtering for every threshold value -- for example, `?threshold=high` includes all four severity counts instead of just critical and high.

2. **No input validation (Criterion 3):** Invalid threshold values (e.g., `?threshold=banana`) are silently handled via `.unwrap_or(0)`, mapping them to index 0 ("critical") instead of returning a 400 Bad Request error. The task requires using `common/src/error.rs::AppError` for validation.

3. **Missing `threshold_applied` field (Criterion 5):** The response does not include a `threshold_applied` boolean field. The `AdvisorySummary` struct was not modified to add this field.

4. **Total field bug:** The `total` field is computed from unfiltered counts (`summary.critical + summary.high + summary.medium + summary.low`) regardless of which severities were filtered out.

**Critical -- Missing test file:**

The task requires creating `tests/api/advisory_summary.rs` with integration tests covering 6 test scenarios (threshold=critical, threshold=high, threshold=medium, no threshold, invalid threshold, non-existent SBOM). This file is entirely absent from the PR diff, leaving the new endpoint behavior with zero automated test coverage.

**Passing criteria:**

- Criterion 2 (backward compatibility): The `None` branch correctly returns the unfiltered summary when no threshold parameter is provided.
- Criterion 6 (404 preservation): The existing SBOM fetch logic is unchanged; non-existent SBOM IDs still produce 404 responses.
