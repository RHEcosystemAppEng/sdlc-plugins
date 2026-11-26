# Criterion 4: Existing pagination and sorting behavior is preserved

**Verdict: FAIL**

## What is preserved
- Offset and limit are still applied in SQL (`.offset(offset.unwrap_or(0))` and the limit), and the `PurlService::recommend(&purl, offset, limit)` signature is unchanged.
- `test_recommend_purls_pagination` is untouched by the diff. It seeds 5 distinct versions, requests `limit=2`, and asserts `items.len()==2` and `total==5`. It still applies, and CI passes.
- When every row simplifies to a distinct PURL, pages behave as before.

## What is broken
The deduplication added for criterion 3 changes pagination behavior in exactly the case this PR introduces: qualifier variants of the same version.
- **Short pages.** Dedup runs on the page after `LIMIT`. With `limit=2` and rows `[3.12?r1, 3.12?r2, 3.11]`, page 1 returns 1 item even though more distinct items exist.
- **Duplicates across pages.** The same simplified PURL can appear on page N and page N+1.
- **`total` no longer matches what a client can page through.** `total` counts pre-dedup purl rows (`group_by(Id)` is a no-op), while `items` are deduplicated.

Before this PR, every row was a distinct item, so `total` and the page contents agreed. This PR breaks that invariant.

## Sorting
- No ORDER BY is visible before or after the change. The PR adds no deterministic sort.
- The new `dedup_by` logic needs a deterministic order to be correct, so behavior now depends on unspecified database order.
- `tests/api/purl_simplify.rs::test_simplified_purl_ordering_preserved` is named for ordering, but it asserts no ordering. It checks only `len()==2`, the absence of `?`, and `total==3`. Sorting preservation is therefore not verified by any test.

## Assessment
Pagination is kept only for inputs without qualifier duplicates, and sorting is not verified. The pagination invariant (total equals the number of distinct items, and pages are complete and do not overlap) is broken for the inputs this change targets. This is covered by the same proposed sub-task as criterion 3.
