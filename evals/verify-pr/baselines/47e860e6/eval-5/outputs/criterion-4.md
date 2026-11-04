# Criterion 4: Existing pagination and sorting behavior is preserved

**Verdict: FAIL**

## Pagination
- **Short pages:** `limit=N` is applied in SQL *before* dedup, so a page can contain fewer than N items even when more distinct results exist.
  - Example: `limit=2` over `[3.12?repo1, 3.12?repo2, 3.11]` returns 1 item.
  - A client that stops when a page has fewer than `limit` items will stop paging too early.
- **Unstable offsets:** `offset` counts raw rows, not deduplicated items. The same simplified PURL can appear on two consecutive pages, and offsets no longer line up with what the client sees.
- **`total` mismatch:** `total` is `select_only().column(purl::Column::Id).group_by(purl::Column::Id).count()`. With the qualifier join removed, `group_by(Id)` changes nothing, so this is the raw row count. It now overcounts the distinct entries a client can actually page through, which gives wrong page counts and empty trailing pages.
- **Tests cannot catch this:** the unchanged `test_recommend_purls_pagination` and the new `test_simplified_purl_ordering_preserved` both seed only distinct versions with one qualifier set each. No duplicates exist, so these regressions are invisible to them.

## Sorting
- The query builder chain (filter, offset, limit, all) has no `order_by`. Result order is whatever PostgreSQL returns, so no sort order is defined that could be "preserved".
- Removing the `LEFT JOIN` can change the query plan and therefore the implicit row order compared with the base branch.
- `test_simplified_purl_ordering_preserved` claims to verify ordering, but it only asserts:
  - `len == 2`
  - no `'?'` in either item
  - `total == 3`

  It never checks which items come back or their order, so ordering is unverified.
- `test_recommend_purls_basic` relies on `items[0]` being 3.12, which depends on the database returning rows in insertion order. That is not guaranteed.

## Conclusion
Pagination becomes inconsistent whenever qualifier variants collapse into duplicates. Sorting is undefined and untested despite a test whose name says otherwise. The criterion is not satisfied.
