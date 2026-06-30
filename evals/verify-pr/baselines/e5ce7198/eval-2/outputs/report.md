## Verification Report for TC-9102 (PR #743)

| Check | Result | Details |
|-------|--------|---------|
| Review Feedback | N/A | No review comments |
| Root-Cause Investigation | N/A | No sub-tasks created |
| Scope Containment | FAIL | `tests/api/advisory_summary.rs` is listed under Files to Create but is entirely absent from the PR diff. Only 2 of 3 required files are present. |
| Diff Size | PASS | Small diff (~50 lines across 2 files). Appropriate scope for the feature. |
| Commit Traceability | PASS | Single commit adding severity threshold filter to advisory summary endpoint, directly aligned with TC-9102 task description. |
| Sensitive Patterns | PASS | No passwords, API keys, private keys, or secrets detected in the diff. |
| CI Status | PASS | All checks pass |
| Acceptance Criteria | FAIL | 3 of 6 criteria met (details below) |
| Test Quality | N/A | No test files present in the PR diff. The required test file `tests/api/advisory_summary.rs` is missing entirely. Eval Quality: N/A |
| Test Change Classification | N/A | No test files in PR diff |
| Verification Commands | N/A | No verification commands specified in the task description |

### Acceptance Criteria Breakdown

| # | Criterion | Result | Finding |
|---|-----------|--------|---------|
| 1 | `?threshold=high` returns counts for critical and high only | FAIL | Filtering logic has inverted comparison: code uses `threshold_idx <= N` but should use `N <= threshold_idx`. For threshold=high (idx=1), medium (1<=2=true) and low (1<=3=true) are incorrectly included. Additionally, the `total` field is computed from unfiltered counts. |
| 2 | Without threshold returns all severity counts (backward compatible) | PASS | The `None` branch returns the unmodified `summary` object. `SummaryParams.threshold` is `Option<String>`, making the parameter optional. |
| 3 | `?threshold=invalid` returns 400 Bad Request | FAIL | Invalid threshold values are silently accepted via `unwrap_or(0)`, which maps unrecognized values to index 0 ("critical"). No validation exists; `AppError` is not used for input validation despite being required by the implementation notes. |
| 4 | Severity ordering correct: critical > high > medium > low | PASS | The ordering array `["critical", "high", "medium", "low"]` correctly encodes the severity hierarchy. (Note: the code that uses this ordering has a separate bug in the comparison direction.) |
| 5 | Response includes `threshold_applied` boolean field | FAIL | The `threshold_applied` field is completely absent. No changes to the `AdvisorySummary` struct are included in the diff, and neither the filtered nor unfiltered response branches set this field. |
| 6 | 404 for non-existent SBOM IDs (existing behavior preserved) | PASS | The existing `SbomService::fetch()` call with `?` error propagation is unchanged, preserving the 404 response for missing SBOMs. |

### Scope Containment Details

**Files to Modify (from task):**
- `modules/fundamental/src/advisory/endpoints/get.rs` -- PRESENT in diff
- `modules/fundamental/src/advisory/service/advisory.rs` -- PRESENT in diff (no substantive changes, but file appears)

**Files to Create (from task):**
- `tests/api/advisory_summary.rs` -- MISSING from diff entirely

The test file is a required deliverable per the task description. Its absence means none of the six test requirements can be verified.

### Key Findings

1. **Missing input validation (Criterion 3)**: The use of `unwrap_or(0)` in `get.rs` silently converts invalid threshold values to "critical" instead of returning 400 Bad Request. The fix is to replace `unwrap_or(0)` with `.ok_or_else(|| AppError::BadRequest(...))? `.

2. **Missing `threshold_applied` field (Criterion 5)**: The response struct `AdvisorySummary` is not modified to include a `threshold_applied: bool` field. This requires changes to the model definition (likely in `modules/fundamental/src/advisory/model/summary.rs`) and both branches of the match expression.

3. **Inverted filtering logic (Criterion 1)**: The comparison `threshold_idx <= N` is backwards. For threshold=high (idx=1): medium passes `1 <= 2` and low passes `1 <= 3`, so they are incorrectly included. The condition should be `N <= threshold_idx` (e.g., include medium only when `2 <= threshold_idx`, which fails for threshold=high since `2 <= 1` is false).

4. **Missing test file (Scope)**: `tests/api/advisory_summary.rs` is listed under "Files to Create" but does not appear in the diff. All six test requirements from the task are unmet.

5. **Incorrect total computation**: The `total` field uses `summary.critical + summary.high + summary.medium + summary.low` (unfiltered counts) even when filtering is applied, producing a total that does not match the filtered severity counts.

### Overall: FAIL

The PR fails verification due to 3 of 6 acceptance criteria not met (Criteria 1, 3, and 5), a missing required test file (`tests/api/advisory_summary.rs`), and a scope containment violation. The implementation has fundamental correctness issues in its filtering logic and input validation that must be addressed before merging.
