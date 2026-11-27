## Verification Report for TC-9105 (commit unknown)

PR: https://github.com/trustify/trustify-backend/pull/746. The head commit SHA was not in the eval inputs, and GitHub was not queried.

| Check | Result | Details |
|-------|--------|---------|
| Review Feedback | N/A | The PR has no review comments and no review bodies. |
| Root-Cause Investigation | DONE | One acceptance-criteria gap sub-task is proposed below. The root cause is a gap in the implement-task phase, with a contributing gap in plan-feature (details below). |
| Scope Containment | PASS | The 4 PR files exactly match Files to Modify (3) and Files to Create (1). No file is out of scope and none is missing. |
| Diff Size | PASS | About 100 lines added and 35 deleted across 4 files, against 4 expected. Proportionate. |
| Commit Traceability | WARN | Commit metadata was not in the eval inputs, so I could not check for references to TC-9105. |
| Sensitive Patterns | PASS | No secrets or credentials in about 100 added lines across 4 files. The only URLs are public repository URLs in test fixtures. |
| CI Status | PASS | All CI checks pass. |
| Acceptance Criteria | FAIL | 3 of 5 criteria met. Criteria 3 (dedup) and 4 (pagination/sorting preserved) fail. |
| Test Quality | PASS | Repetitive tests: PASS. Test documentation: PASS (all 7 test functions have `///` doc comments). Eval Quality: N/A. |
| Test Change Classification | MIXED | `purl_recommend.rs`: -1 test function (`test_recommend_purls_with_qualifiers`), +1 (`test_recommend_purls_dedup`), -6/+7 assertions, and the expected value in `test_recommend_purls_basic` changed. The new `purl_simplify.rs` adds 3 tests. |
| Verification Commands | N/A | The task specifies none, and no eval infrastructure changed. |

### Overall: FAIL

### Acceptance Criteria

| # | Criterion | Result |
|---|---|---|
| 1 | Recommend endpoint returns versioned PURLs without qualifiers | PASS |
| 2 | Response PURLs contain no `?` qualifiers | PASS |
| 3 | Qualifier-only duplicates are deduplicated | FAIL |
| 4 | Existing pagination and sorting behavior is preserved | FAIL |
| 5 | Response shape is still `PaginatedResults<PurlSummary>` | PASS |

Detailed reasoning for each criterion is in `criterion-1.md` to `criterion-5.md`.

### Issues requiring attention

1. **Dedup is incomplete (AC3).** In `PurlService::recommend` (`modules/fundamental/src/purl/service/mod.rs`), dedup uses `.dedup_by(|a, b| a.purl == b.purl)` on the Rust iterator.
   - It removes only *adjacent* duplicates, and the query has no `ORDER BY`, so duplicates are not guaranteed to be adjacent.
   - It runs *after* SQL `OFFSET`/`LIMIT`, so duplicates that fall on different pages survive.
2. **Pagination changed (AC4).**
   - `total` counts raw `purl.id` rows (`group_by(Id).count()`), not deduplicated PURLs. In the PR's own dedup scenario, `items.len() == 1` but `total == 2`.
   - Pages can hold fewer than `limit` items even when more distinct results exist.
   - No deterministic sort order exists.
3. **Some tests claim more than they assert.**
   - `test_recommend_purls_dedup` does not assert `total`, and it does not cover non-adjacent or cross-page duplicates.
   - `test_simplified_purl_ordering_preserved` does not assert any ordering.
4. **Test changes are MIXED (informational).** The test changes are partly reductive. Removing `test_recommend_purls_with_qualifiers` and changing the expected value in `test_recommend_purls_basic` are both explicitly required by the task, because qualifier behavior is removed on purpose. So the reductive signals are justified and are not a defect. The new dedup test and the new `purl_simplify.rs` file add coverage for the new behavior.
5. **Two things CI implies but the diff does not show.**
   - `dedup_by` needs `itertools::Itertools` in scope, and the diff adds no such import.
   - The diff adds no `mod purl_simplify;` registration for the new test file.
   - Since CI passes, both are presumably handled outside the diff, but a reviewer should confirm that the new tests actually run.

### Proposed sub-task (not created; this eval writes to files only)

- **Type:** Sub-task of TC-9105. Labels `ai-generated-jira`, `review-feedback`. Link: Blocks TC-9105.
- **Summary:** Deduplicate simplified PURL recommendations in SQL before OFFSET/LIMIT, align `total`, and add deterministic ordering.
- **Files:** `modules/fundamental/src/purl/service/mod.rs`, `tests/api/purl_recommend.rs`, `tests/api/purl_simplify.rs`
- **Acceptance Criteria:**
  - Recommendations are deduplicated on version-level identity (type/namespace/name/version) in SQL, before pagination.
  - The query has an explicit `ORDER BY`.
  - `total` is computed over the same distinct set as `items`.
  - `test_recommend_purls_dedup` asserts `total == 1`.
  - New tests cover duplicates that are non-adjacent and duplicates that cross a page boundary.
  - `test_simplified_purl_ordering_preserved` asserts the order of the items.
- **Target PR:** https://github.com/trustify/trustify-backend/pull/746

### Root-cause analysis

- **Defect:** dedup was applied in memory after pagination, using adjacent-only semantics, and `total` was not reconciled with the deduplicated items.
- **Universality test:** universal. Any paginated API that deduplicates or filters must do it before offset and limit, and must compute `total` over the same set.
- **Method vs. fact:** method. The guidance is "apply transformations that change cardinality before pagination, and keep the total consistent with the items". It needs no language-specific API, so this is a **skill gap**.
- **Phase:**
  - Primarily **implement-task**. The task stated the dedup requirement and that pagination must be preserved, but the implementation did not check how dedup interacts with pagination.
  - Contributing: **plan-feature**. The Implementation Notes asked for a dedup *test* but did not say where dedup should happen or how `total` should behave.
- **Proposed root-cause task:** "Root-cause: implement-task should verify that cardinality-changing transforms (dedup, filter) run before pagination and that totals stay consistent with the returned items." Labels `ai-generated-jira`, `root-cause`. Link: Relates to TC-9105. Not created, because this is an offline eval.

---
*This comment was AI-generated by [sdlc-workflow/verify-pr](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.14.0.*
