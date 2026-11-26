## Verification Report for TC-9102 (commit unknown)

PR: https://github.com/trustify/trustify-backend/pull/743. The head commit SHA was not available in the eval inputs.

| Check | Result | Details |
|-------|--------|---------|
| Review Feedback | N/A | The PR has no review comments or review bodies |
| Root-Cause Investigation | DONE | The gap comes from the implement-task phase. The task spec was explicit and the implementation did not follow its acceptance criteria and test requirements (see Root-Cause section) |
| Scope Containment | FAIL | `tests/api/advisory_summary.rs` (Files to Create) is missing. `advisory/service/advisory.rs` appears in the diff but has no changed lines, so the filtering logic expected there was not implemented. No out-of-scope files |
| Diff Size | PASS | About 26 lines changed (+25/-1) in 1 substantive file, against 3 expected files. Proportionate (if anything undersized) |
| Commit Traceability | WARN | Commit data was not available in the inputs, so references to TC-9102 could not be verified |
| Sensitive Patterns | PASS | No secrets, credentials or sensitive patterns in the 25 added lines |
| CI Status | PASS | All CI checks pass |
| Acceptance Criteria | FAIL | 3 of 6 criteria met (criteria 2, 4 and 6 met; criteria 1, 3 and 5 not met) |
| Test Quality | N/A | No test files in the PR (Repetitive Tests: N/A, Test Documentation: N/A). Eval Quality: N/A |
| Test Change Classification | N/A | No test files added, modified or deleted |
| Verification Commands | N/A | The task specifies no verification commands |

### Overall: FAIL

### Acceptance Criteria Detail

| # | Criterion | Result | Reason |
|---|---|---|---|
| 1 | `?threshold=high` returns counts for critical and high only | NOT MET | Medium and low are zeroed rather than omitted, and `total` is computed from the **unfiltered** counts (`summary.critical + summary.high + summary.medium + summary.low`), so it contradicts the filtered fields |
| 2 | No threshold returns all severity counts (backward compatible) | MET | `threshold: Option<String>`. The `None => summary` branch returns the original response unchanged |
| 3 | `?threshold=invalid` returns 400 Bad Request | NOT MET | `.position(...).unwrap_or(0)` silently treats an invalid value as `critical` and returns 200. No `AppError` validation |
| 4 | Severity ordering critical > high > medium > low | MET | The ordered array and `<=` index gating give correct inclusion for valid values. Deviation: no `Severity` enum implementing `Ord`, which the implementation notes require |
| 5 | Response includes a `threshold_applied` boolean | NOT MET | The field is absent from the response struct and the handler. The model file is not modified |
| 6 | 404 for non-existent SBOM IDs (existing behavior preserved) | MET | The SBOM fetch and not-found path are unchanged. No 404 test was added |

Detailed per-criterion reasoning is in `criterion-1.md` through `criterion-6.md`.

### Issues Requiring Attention

1. **Invalid threshold is not rejected (AC 3).** `unwrap_or(0)` in `modules/fundamental/src/advisory/endpoints/get.rs` must be replaced with strict parsing that returns `AppError` (400). A `Severity` enum with `FromStr`/`Deserialize` and `Ord` would meet both this criterion and the implementation notes.
2. **`threshold_applied` field is missing (AC 5).** Add it to `AdvisorySummary` (`modules/fundamental/src/advisory/model/summary.rs`) and set it in the handler.
3. **Filtered response is incorrect (AC 1).** `total` must be computed from the filtered counts, and below-threshold severities should be omitted rather than reported as `0`. The implementation notes ask for this filtering in the aggregation query in `advisory.rs` (an optional WHERE on severity rank). That file's hunk contains no changes.
4. **No tests (Test Requirements).** `tests/api/advisory_summary.rs` was not created. None of the 6 required tests exist (threshold=critical/high/medium, no threshold, invalid → 400, missing SBOM → 404).
5. **Commit traceability could not be verified.** No commit data was available.

### Sub-tasks (proposed; not created in Jira because this is an offline eval)

Each would be created as a Sub-task of TC-9102 with labels `["ai-generated-jira", "review-feedback"]`, a "Blocks" link to TC-9102, and Target PR https://github.com/trustify/trustify-backend/pull/743:

1. Reject invalid `threshold` values on advisory-summary with 400 Bad Request. Files: `modules/fundamental/src/advisory/endpoints/get.rs`, `common/src/error.rs`
2. Add `threshold_applied` boolean to the advisory-summary response. Files: `modules/fundamental/src/advisory/model/summary.rs`, `modules/fundamental/src/advisory/endpoints/get.rs`
3. Compute `total` from the filtered counts, omit below-threshold severities, and move filtering into the aggregation query. Files: `modules/fundamental/src/advisory/endpoints/get.rs`, `modules/fundamental/src/advisory/service/advisory.rs`
4. Add `tests/api/advisory_summary.rs` covering the threshold filtering cases. Files: `tests/api/advisory_summary.rs`

### Root-Cause Investigation

- **Classification:** universal method, so a skill gap. "Verify every acceptance criterion and test requirement is implemented before opening a PR; validate input instead of silently defaulting" applies to any repository and is language-agnostic.
- **Phase:** implement-task. The Feature-to-task chain was sound: the task spelled out the 400 behavior, the `threshold_applied` field, the `Severity` enum, the location of the filtering in the service, and the test file. The implementation skipped them.
- **Proposed root-cause task:** "Root-cause: implement-task should perform an acceptance-criteria and Files-to-Create self-check before pushing." Labels `["ai-generated-jira", "root-cause"]`, linked to TC-9102 with "Relates". Not created (offline eval).

---
*This comment was AI-generated by [sdlc-workflow/verify-pr](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.14.0.*
