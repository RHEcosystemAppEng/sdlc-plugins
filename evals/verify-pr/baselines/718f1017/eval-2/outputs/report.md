## Verification Report for TC-9102

**Task**: Add severity threshold filter to advisory summary endpoint
**PR**: #743 (trustify-backend)

| Check | Result | Details |
|-------|--------|---------|
| Review Feedback | N/A | No review comments on the PR |
| Root-Cause Investigation | N/A | No sub-tasks created |
| Scope Containment | FAIL | PR modifies 2 of 2 expected files but is missing the required new file `tests/api/advisory_summary.rs` |
| Diff Size | PASS | ~26 lines changed across 2 files; proportional to task scope |
| Commit Traceability | PASS | Single commit addresses TC-9102 |
| Sensitive Patterns | PASS | No secrets, credentials, tokens, or hardcoded keys detected in the diff |
| CI Status | PASS | All CI checks pass |
| Acceptance Criteria | FAIL | 3 of 6 criteria met; 3 criteria FAIL (see Correctness section) |
| Test Quality | N/A | No test files present in the diff to evaluate |
| Test Change Classification | N/A | No test files in PR diff |
| Verification Commands | N/A | No verification commands specified in the task |

### Overall: FAIL

Three acceptance criteria are not satisfied, and the required test file is entirely absent from the diff.

### Intent Alignment

**Files expected to be modified (per task spec):**

| Expected File | In Diff? | Notes |
|---|---|---|
| `modules/fundamental/src/advisory/endpoints/get.rs` | Yes | Modified to add `SummaryParams` struct and threshold filtering logic |
| `modules/fundamental/src/advisory/service/advisory.rs` | Yes | Present in diff but contains no functional changes (only context lines shown) |

**Files expected to be created (per task spec):**

| Expected File | In Diff? | Notes |
|---|---|---|
| `tests/api/advisory_summary.rs` | **No** | Completely absent from the diff; no integration tests were added |

The task explicitly requires creating `tests/api/advisory_summary.rs` with integration tests for threshold filtering. This file is not present anywhere in the diff. The repository structure shows the `tests/api/` directory exists and already contains test files (`sbom.rs`, `advisory.rs`, `search.rs`), so the pattern is well-established and should have been followed.

### Security

No sensitive patterns detected in the diff:
- No hardcoded credentials, API keys, or tokens
- No `.env` file changes
- No secret-like strings or connection strings
- No changes to authentication or authorization logic
- The endpoint handler follows the existing error handling pattern with `AppError`

### Correctness

**Criterion 1: `?threshold=high` returns counts for critical and high only** -- PASS
The filtering logic uses a `severity_order` array and index comparison to zero out severity counts below the threshold. When `threshold=high`, `threshold_idx` is 1, so `high` (idx <= 1) is included and lower severities are zeroed out.

**Criterion 2: No threshold returns all severity counts (backward compatible)** -- PASS
The `None` arm of the match returns the unmodified `summary`, preserving backward compatibility.

**Criterion 3: `?threshold=invalid` returns 400 Bad Request** -- FAIL
The implementation uses `.unwrap_or(0)` when looking up the threshold value in the severity array. An invalid threshold string (e.g., "invalid") will silently default to index 0, which corresponds to "critical" filtering. The task explicitly requires returning a 400 Bad Request error. The implementation notes reference `common/src/error.rs::AppError` for validation errors, but this is not used.

**Criterion 4: Severity ordering correct: critical > high > medium > low** -- PASS
The `severity_order` array `["critical", "high", "medium", "low"]` correctly encodes the ordering with critical at index 0 (highest) and low at index 3 (lowest).

**Criterion 5: Response includes `threshold_applied` boolean field** -- FAIL
The `AdvisorySummary` struct construction in the filtering logic includes only `critical`, `high`, `medium`, `low`, and `total` fields. There is no `threshold_applied` boolean field added to the response. The task explicitly requires this field to indicate whether filtering is active.

**Criterion 6: 404 for non-existent SBOM IDs (existing behavior preserved)** -- PASS
The existing `.ok_or(AppError::NotFound)` pattern on the SBOM fetch is preserved in the diff context, so 404 behavior for non-existent SBOMs is maintained.

**Additional issue noted**: The `total` field in the filtered response is computed as `summary.critical + summary.high + summary.medium + summary.low`, which sums the unfiltered counts. It should sum only the counts that remain after filtering to be consistent with the filtered output.

### Style/Conventions

- The `SummaryParams` struct follows the existing query parameter pattern (consistent with `list.rs` patterns in the codebase)
- The `Deserialize` derive and `serde` import are appropriate
- Error handling follows the `Result<T, AppError>` convention for the handler signature
- No test files are present in the diff, so test quality and test change classification are N/A
