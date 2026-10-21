## Verification Report for TC-9102 (PR #743)

| Check | Result | Details |
|-------|--------|---------|
| Review Feedback | N/A | No review comments exist on this PR |
| Root-Cause Investigation | N/A | No sub-tasks created; nothing to investigate |
| Scope Containment | FAIL | 1 task-required file missing from PR: `tests/api/advisory_summary.rs` |
| Diff Size | PASS | 2 files changed, proportionate to task scope (3 expected files, 2 present) |
| Commit Traceability | PASS | Commits reference TC-9102 |
| Sensitive Patterns | PASS | No sensitive patterns detected in added lines |
| CI Status | PASS | All CI checks pass |
| Acceptance Criteria | FAIL | 3 of 6 criteria not met |
| Test Quality | N/A | No test files in PR diff; Eval Quality: N/A |
| Test Change Classification | N/A | No test files exist in the PR diff |
| Verification Commands | N/A | No verification commands specified in task |

### Overall: FAIL

This PR fails verification due to two FAIL-level checks: **Scope Containment** and **Acceptance Criteria**.

---

## Detailed Findings

### Scope Containment -- FAIL

**Details:** The task specifies 3 files (2 to modify, 1 to create). The PR modifies the 2 existing files but does not create the required test file.

**PR files:**
- `modules/fundamental/src/advisory/endpoints/get.rs` (modified)
- `modules/fundamental/src/advisory/service/advisory.rs` (modified)

**Task-specified files:**
- `modules/fundamental/src/advisory/endpoints/get.rs` (modify) -- present
- `modules/fundamental/src/advisory/service/advisory.rs` (modify) -- present
- `tests/api/advisory_summary.rs` (create) -- MISSING

**Unimplemented files:** `tests/api/advisory_summary.rs` -- the task explicitly requires this file to be created with integration tests for threshold filtering. The repository's existing test structure (`tests/api/sbom.rs`, `tests/api/advisory.rs`, `tests/api/search.rs`) confirms this is the standard location for endpoint integration tests. None of the six test requirements from the task are covered.

**Out-of-scope files:** None

### Diff Size -- PASS

**Details:** The change is proportionate to the task scope.

**Evidence:**
- Files changed: 2
- Expected file count: 3 (2 modify + 1 create)
- The additions are modest: a new query parameter struct, threshold filtering logic in the handler, and a minor touch to the service file
- The change size is consistent with adding an optional query parameter to an existing endpoint

### Commit Traceability -- PASS

**Details:** PR commits reference the Jira task ID TC-9102.

### Sensitive Patterns -- PASS

**Details:** No sensitive patterns detected in added lines across 2 files. Scanned all added lines in the PR diff for hardcoded passwords, API keys, private keys, environment files, cloud credentials, and database credentials. No matches found.

### CI Status -- PASS

**Details:** All CI checks pass. No failing or pending checks.

### Acceptance Criteria -- FAIL

3 of 6 acceptance criteria are not satisfied. Per-criterion details are in the criterion-N.md files.

| # | Criterion | Result | Gap |
|---|-----------|--------|-----|
| 1 | threshold=high returns critical and high only | FAIL | Filtering logic is inverted (`threshold_idx <= N` instead of `N <= threshold_idx`); with threshold=high, medium and low counts are also returned |
| 2 | Without threshold returns all severity counts | PASS | None branch returns original summary unchanged |
| 3 | threshold=invalid returns 400 Bad Request | FAIL | `unwrap_or(0)` silently maps invalid values to index 0 (critical) instead of returning 400 via AppError |
| 4 | Severity ordering correct | PASS | Array `["critical", "high", "medium", "low"]` correctly represents the ordering |
| 5 | Response includes threshold_applied boolean | FAIL | Field is completely absent from AdvisorySummary struct and response construction |
| 6 | Returns 404 for non-existent SBOM IDs | PASS | Existing SbomService::fetch 404 behavior is preserved |

#### Key gaps identified:

**Gap 1 -- Invalid threshold silently accepted (Criterion 3):** The code at `get.rs` line 45-46 uses `.unwrap_or(0)` on the result of `severity_order.iter().position()`. When a caller passes an invalid threshold value (e.g., `?threshold=invalid`), `position()` returns `None`, and `unwrap_or(0)` silently treats it as index 0 (critical). The task explicitly requires returning HTTP 400 Bad Request for invalid values, and the implementation notes reference `common/src/error.rs::AppError` for this purpose. The `AppError` type is imported but never used for threshold validation.

**Gap 2 -- Missing threshold_applied boolean (Criterion 5):** The `AdvisorySummary` struct in the response contains only `critical`, `high`, `medium`, `low`, and `total` fields. The task requires a `threshold_applied` boolean field indicating whether filtering is active. This field is absent from both the struct definition (in `model/summary.rs`, which is not modified in this PR) and the response construction in `get.rs`. API consumers have no way to determine from the response whether threshold filtering was applied.

**Gap 3 -- Missing test file (Scope Containment):** The task specifies creating `tests/api/advisory_summary.rs` with integration tests covering six test requirements (threshold=critical, threshold=high, threshold=medium, no threshold, invalid threshold, non-existent SBOM). This file is entirely absent from the PR diff. The repository has an established pattern of integration tests in `tests/api/` (e.g., `sbom.rs`, `advisory.rs`, `search.rs`), and no test coverage for the new threshold filtering functionality exists.

### Test Quality -- N/A

**Details:** No test files exist in the PR diff. The PR modifies only production code files. Repetitive Test Detection: N/A. Test Documentation: N/A. Eval Quality: N/A (no eval result reviews found on this PR).

### Test Change Classification -- N/A

**Details:** No test files exist in the PR diff. The task requires creating `tests/api/advisory_summary.rs`, but this file is absent. Since no test files were added, modified, or deleted, classification is not applicable.

### Verification Commands -- N/A

**Details:** No verification commands were specified in the task description.
