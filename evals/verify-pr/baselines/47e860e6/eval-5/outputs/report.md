## Verification Report for TC-9105 (commit unknown — HEAD SHA not available in eval inputs)

| Check | Result | Details |
|-------|--------|---------|
| Review Feedback | N/A | The PR has no inline comments and no review bodies. |
| Root-Cause Investigation | DONE | One defect from the acceptance-criteria check (dedup and pagination). Classified as a universal method, so it is a skill gap in the implement-task phase. A root-cause task would be created; see below. |
| Scope Containment | PASS | The 4 changed files exactly match the task's 3 Files to Modify and 1 File to Create. None are extra and none are missing. |
| Diff Size | PASS | +100 / -35 across 4 files, in proportion to the task. |
| Commit Traceability | N/A | The eval inputs had no commit data, so TC-9105 references could not be checked. |
| Sensitive Patterns | PASS | No secrets or credentials. The only URLs are public registry addresses in test PURL qualifiers. |
| CI Status | PASS | All CI checks pass. |
| Acceptance Criteria | FAIL | 3 of 5 criteria met. Criteria 3 (dedup) and 4 (pagination/sorting preserved) fail. |
| Test Quality | PASS | Repetitive Test Detection: PASS. Test Documentation: PASS (all 6 new or changed tests have `///` doc comments). Eval Quality: N/A. |
| Test Change Classification | MIXED | `purl_recommend.rs`: `test_recommend_purls_with_qualifiers` removed (5 assertions), `test_recommend_purls_dedup` added, `test_recommend_purls_basic` assertions changed to the qualifier-free form. `purl_simplify.rs` is new (3 tests). The removal is explicitly required by the task, so the reductive part is intended. |
| Verification Commands | N/A | The task has no Verification Commands section, and the PR does not touch eval infrastructure. |

### Overall: FAIL

#### Acceptance Criteria detail

| # | Criterion | Result |
|---|---|---|
| 1 | Returns versioned PURLs without qualifiers | PASS |
| 2 | Response PURLs have no `?` qualifiers | PASS |
| 3 | Duplicates that differed only by qualifiers are deduplicated | FAIL |
| 4 | Existing pagination and sorting behavior preserved | FAIL |
| 5 | Response shape still `PaginatedResults<PurlSummary>` | PASS |

The reasoning for each criterion is in `criterion-1.md` to `criterion-5.md`.

#### Issues requiring attention

In `modules/fundamental/src/purl/service/mod.rs`, `PurlService::recommend` has four problems:

1. **Dedup only removes adjacent duplicates.** `.dedup_by(|a, b| a.purl == b.purl)` removes only consecutive equal items, and the query has no `ORDER BY`.
   - Example: rows `3.12?repo1`, `3.11`, `3.12?repo2` produce `[3.12, 3.11, 3.12]`, and the duplicate stays.
2. **Dedup runs after SQL `OFFSET`/`LIMIT`.**
   - Duplicates that cross a page boundary are never removed.
   - Pages can come back with fewer than `limit` items while more data exists.
   - Offsets no longer line up with the items a client actually sees.
3. **`total` overcounts.** `total` counts raw purl rows (`group_by(Id)` changes nothing once the join is gone), not the deduplicated entries. In the dedup test's own scenario, the response has `items.len() == 1` but `total == 2`.
4. **No sort order is defined.** The query has no `ORDER BY`. `test_simplified_purl_ordering_preserved` asserts no ordering at all, and `test_recommend_purls_basic` depends on `items[0]` being 3.12.

**Test gaps.** `test_recommend_purls_dedup` seeds only two duplicates, which are always adjacent and on one page. It does not assert `total`. No test covers non-adjacent duplicates or duplicates across a page boundary.

#### Sub-task (would be created; not posted because the eval allows no external services)

- **Summary:** Make PURL recommendation dedup global, apply it before pagination, align `total`, and define the sort order
- **Labels:** `ai-generated-jira`, `review-feedback`
- **Parent:** TC-9105. **Link:** Blocks TC-9105.
- **Target PR:** https://github.com/trustify/trustify-backend/pull/746
- **Relevant files:**
  - `modules/fundamental/src/purl/service/mod.rs`
  - `tests/api/purl_recommend.rs`
  - `tests/api/purl_simplify.rs`
- **Fix:**
  - Deduplicate in SQL with `DISTINCT` or `GROUP BY` on the qualifier-free identity (type/namespace/name/version).
  - Add a deterministic `ORDER BY`.
  - Apply offset/limit and compute `total` over that same distinct set.
- **Tests to add:**
  - Non-adjacent duplicates.
  - Duplicates across a `limit`/`offset` boundary.
  - `total` after dedup.
  - Real ordering assertions in `test_simplified_purl_ordering_preserved`.

#### Root-cause investigation

- **Universality test:** universal. Any paginated list endpoint that removes duplicates has the same requirement: deduplicate over the whole result set before paginating, and keep `total` consistent with the deduplicated items.
- **Method-vs-Fact test:** method. The guidance can be stated without naming a language, for example: "when post-processing removes items from a paginated query, verify the reduction happens before offset/limit and that the total count reflects it; verify order-dependent operations have a defined order." It is therefore a skill gap, not a convention gap.
- **Phase:**
  - Define-feature: no gap.
  - Plan-feature: no gap. The task stated the requirement in AC 3 and AC 4, and the Implementation Notes flagged that duplicates may appear.
  - Implement-task: gap. The implementation added in-memory, adjacent-only dedup after pagination and did not check it against the "pagination preserved" criterion.
- **Root-cause task (would be created):**
  - **Summary:** "Root-cause: implement-task should verify that post-query filtering/dedup is pagination- and count-consistent and that order-dependent operations have a defined order"
  - **Labels:** `ai-generated-jira`, `root-cause`
  - **Link:** Relates to TC-9105
  - **Comment:** "Root-cause analysis from TC-9105 verification"

---
*This comment was AI-generated by [sdlc-workflow/verify-pr](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.10.*
