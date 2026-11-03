## Verification Report for TC-9102 (commit unavailable)

PR: https://github.com/trustify/trustify-backend/pull/743. The eval input has no head commit SHA, so the header shows "unavailable".

| Check | Result | Details |
|-------|--------|---------|
| Review Feedback | N/A | The PR has no inline review comments and no review bodies |
| Root-Cause Investigation | N/A | Step 6d created no sub-tasks: there was no review feedback, CI passed, and there were no eval failures |
| Scope Containment | FAIL | The required new file `tests/api/advisory_summary.rs` is missing. `modules/fundamental/src/advisory/service/advisory.rs` is listed in the diff, but its only hunk has context lines and no changes, so the service-layer filtering the task asked for was not done. No files outside the task scope were touched |
| Diff Size | PASS | +25/-1 across 2 files (only `get.rs` has real changes); the task expected 3 files |
| Commit Traceability | N/A | The eval input has no commit data, so traceability to TC-9102 could not be checked |
| Sensitive Patterns | PASS | Scanned 25 added lines and found no secrets, credentials, keys or connection strings |
| CI Status | PASS | All CI checks pass on the PR head (from the eval input). No new tests were added, so CI does not exercise the new behavior |
| Acceptance Criteria | FAIL | 2 of 6 criteria met. AC1, AC3, AC4 and AC5 are not met |
| Test Quality | N/A | No test files in the PR. Repetitive Tests: N/A; Test Documentation: N/A; Eval Quality: N/A |
| Test Change Classification | N/A | No test files were added, modified or deleted |
| Verification Commands | N/A | The task has no Verification Commands section, and the PR does not change eval infrastructure |

### Acceptance Criteria Detail

| # | Criterion | Result | Key evidence |
|---|---|---|---|
| 1 | `?threshold=high` returns critical and high only | FAIL | The comparisons are inverted (`threshold_idx <= 2` keeps medium when idx=1, and `threshold_idx <= 3` keeps low), so all four counts come back. `total` is also summed from unfiltered counts. See `criterion-1.md` |
| 2 | No threshold returns all counts (backward compatible) | PASS | `threshold: Option<String>`; `None => summary` returns the original aggregate unchanged. See `criterion-2.md` |
| 3 | `?threshold=invalid` returns 400 | FAIL | `.position(...).unwrap_or(0)` treats unknown values as `critical` and returns 200. No `AppError` validation path exists. See `criterion-3.md` |
| 4 | Ordering critical > high > medium > low | FAIL | The array order is right but the index checks run the wrong way, so every threshold gives the wrong set. No `Severity` enum with `Ord` was defined. See `criterion-4.md` |
| 5 | Response includes `threshold_applied` boolean | FAIL | The field is set in neither branch. `model/summary.rs` is not modified. See `criterion-5.md` |
| 6 | 404 for non-existent SBOM preserved | PASS | The SBOM lookup and error path are unchanged, and the new optional `Query` extractor does not block it. No test was added. See `criterion-6.md` |

Test Requirements coverage: 0 of 6. `tests/api/advisory_summary.rs` was not created, and no tests exist for critical, high or medium thresholds, the no-threshold case, the invalid value returning 400, or the missing SBOM returning 404.

### Overall: FAIL

The PR adds the `threshold` query parameter to the advisory summary handler but fails most of the functional requirements:

1. **Inverted threshold filtering (AC1, AC4).** In `modules/fundamental/src/advisory/endpoints/get.rs`, the checks `threshold_idx <= 1/2/3` compare in the wrong direction. A severity at index `i` should be kept when `i <= threshold_idx`. As written, `threshold=critical` and `threshold=high` return all four counts, and `threshold=medium` and `threshold=low` drop the higher severities.
2. **Wrong `total`.** It is computed from the unfiltered `summary.*` values, not the filtered counts.
3. **No input validation (AC3).** `unwrap_or(0)` accepts any invalid threshold and returns 200 instead of a 400 `AppError`.
4. **Missing `threshold_applied` field (AC5).** It was not added to `AdvisorySummary` or to the response.
5. **Implementation deviates from the plan.** There is no `Severity` enum with `Ord`, and no WHERE clause on severity rank in `AdvisoryService` aggregation (`service/advisory.rs` is unchanged). The filtering was done in the handler after aggregation.
6. **No tests.** The required file `tests/api/advisory_summary.rs` is missing, so none of the 6 test requirements are covered. Passing CI says nothing about the new behavior.

Recommended follow-up (for the implementer or the reviewer): fix the comparison direction and use a `Severity` enum with `Ord`, recompute `total` from the filtered counts, return 400 through `AppError` for unknown thresholds, add `threshold_applied` to the response, move the filtering into `AdvisoryService` aggregation as the task specifies, and create `tests/api/advisory_summary.rs` covering all 6 test requirements. Under this skill's rules, failed acceptance criteria are reported here rather than turned into review-feedback sub-tasks, so no Jira sub-tasks were created. Per the eval constraints, nothing was posted to Jira or GitHub.

---
*This comment was AI-generated by [sdlc-workflow/verify-pr](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.10.*
