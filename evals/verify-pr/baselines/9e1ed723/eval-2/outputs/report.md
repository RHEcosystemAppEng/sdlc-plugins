## Verification Report for TC-9102 (commit n/a)

PR: https://github.com/trustify/trustify-backend/pull/743. Task: Add severity threshold filter to advisory summary endpoint.

| Check | Result | Details |
|-------|--------|---------|
| Review Feedback | N/A | PR has no review comments and no review bodies |
| Root-Cause Investigation | N/A | No sub-tasks were created in Step 6d (no review feedback, no CI failures), so there was nothing to investigate |
| Scope Containment | FAIL | Unimplemented: `tests/api/advisory_summary.rs` (Files to Create) is missing. `modules/fundamental/src/advisory/service/advisory.rs` shows up in the diff with context lines only (0 additions, 0 deletions), so the aggregation-query change was not made. No out-of-scope files |
| Diff Size | PASS | About 24 additions and 1 deletion across 2 files (3 expected). Size fits the scope; if anything the PR is under-implemented |
| Commit Traceability | WARN | PR commit metadata was not in the inputs provided, so references to TC-9102 could not be confirmed |
| Sensitive Patterns | PASS | No secrets, credentials, tokens, private keys or unsafe patterns in the added lines |
| CI Status | PASS | All CI checks pass |
| Acceptance Criteria | FAIL | 2 of 6 criteria met (criteria 1, 3, 4 and 5 fail) |
| Test Quality | N/A | No test files in the PR diff. Repetitive Test Detection: N/A. Test Documentation: N/A. Eval Quality: N/A (no eval result reviews) |
| Test Change Classification | N/A | No test files were added, modified or deleted |
| Verification Commands | N/A | The task has no Verification Commands section and no eval infrastructure files changed |

### Overall: FAIL

### Acceptance Criteria Detail

| # | Criterion | Result | Summary |
|---|---|---|---|
| 1 | `?threshold=high` returns counts for critical and high only | FAIL | The filter comparisons are inverted (`threshold_idx <= i` where `i <= threshold_idx` is needed), so `threshold=high` still returns medium and low. `total` is always the unfiltered sum. See criterion-1.md |
| 2 | No threshold returns all severity counts (backward compatible) | PASS | `threshold: Option<String>`. The `None => summary` arm returns the aggregate unchanged. See criterion-2.md |
| 3 | `?threshold=invalid` returns 400 Bad Request | FAIL | `.position(...).unwrap_or(0)` quietly maps unknown values to `critical` and returns 200. No `AppError` validation. See criterion-3.md |
| 4 | Severity ordering is correct: critical > high > medium > low | FAIL | The array order is right, but the inverted comparisons apply it backwards (`threshold=low` gives critical+low only, `threshold=critical` gives everything). No `Severity` enum implementing `Ord` was added. See criterion-4.md |
| 5 | Response includes `threshold_applied` boolean | FAIL | The field is not in the response struct or the handler. See criterion-5.md |
| 6 | 404 for non-existent SBOM IDs preserved | PASS | The SBOM fetch and error path are unchanged and run before the new logic. See criterion-6.md |

### Issues Requiring Attention

1. **Threshold filtering is inverted.** In `modules/fundamental/src/advisory/endpoints/get.rs` the conditions `if threshold_idx <= N` keep a bucket when the threshold is *above* it in the list. They should keep it when it is at or above the threshold. As written, `critical` and `high` thresholds do no filtering, and `medium`/`low` drop the wrong buckets.
2. **`total` is not filtered.** It is computed from the original `summary` fields, not the filtered values.
3. **No validation of invalid thresholds.** `unwrap_or(0)` swallows bad input. The task requires a 400 through `AppError`, ideally by deserializing into the `Severity` enum the Implementation Notes ask for.
4. **The `threshold_applied` field is missing** from the response.
5. **The `Severity` enum implementing `Ord` was not added.** An ad-hoc string array is used instead.
6. **Filtering is not in the aggregation query.** The Implementation Notes ask for an optional WHERE clause on severity rank in `advisory.rs`. That file has no real changes and filtering happens after aggregation in the handler.
7. **No tests.** `tests/api/advisory_summary.rs` was not created, so none of the six Test Requirements are met (threshold=critical/high/medium, no threshold, invalid → 400, missing SBOM → 404).

Note: under verify-pr rules, acceptance-criteria failures are reported here and do not create sub-tasks automatically. Sub-tasks are only created for review-feedback code change requests and CI failures, and this PR has neither. The PR needs more implementation work before merge.

### Domain Findings Summary

- **Intent Alignment:** Scope Containment FAIL (required test file missing; service file not really changed). Diff Size PASS. Commit Traceability WARN (no commit data provided).
- **Security:** Sensitive Pattern Scan PASS. Only query-parameter parsing and in-memory filtering were added. No secrets, no raw SQL, no unsafe code.
- **Correctness:** CI Status PASS. Acceptance Criteria FAIL (2/6). Verification Commands N/A.
- **Style/Conventions:** Convention Upgrade N/A (no suggestions to upgrade). Repetitive Test Detection N/A. Test Documentation N/A. Eval Quality N/A. Test Change Classification N/A. Minor deviation: the task asked to follow the query parameter pattern in `advisory/endpoints/list.rs`; the `SummaryParams` struct with `Query<...>` matches that pattern on the surface, but validation is missing. Repository `CONVENTIONS.md` content was not available in the eval inputs.

---
*This comment was AI-generated by [sdlc-workflow/verify-pr](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.14.0.*
