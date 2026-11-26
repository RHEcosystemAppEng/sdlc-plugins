# Criterion 4: Existing pagination and sorting behavior is preserved

**Verdict: PASS (with a caveat tied to Criterion 3)**

## What was checked
- **Pagination:** `query.offset(offset.unwrap_or(0) as u64)` and the `limit` clause are unchanged in
  `PurlService::recommend`. The handler still passes `params.offset` and `params.limit` through.
- **Total count:** the plain `query.clone().count()` became a count grouped by `purl::Column::Id`.
  With the qualifier join removed, each purl row now appears once, so the count matches the number
  of purl rows. Before, the LEFT JOIN on qualifiers could inflate it.
- **Sorting:** the diff adds or removes no `order_by`. Whatever ordering the query had before
  (implicit or defined outside the changed hunk) is unchanged.
- **Tests:** `test_recommend_purls_pagination` (5 versions, `limit=2`, asserts `items.len() == 2` and
  `total == 5`) and `test_recommend_purls_unknown_returns_empty` are kept unchanged in
  `tests/api/purl_recommend.rs`. The new
  `tests/api/purl_simplify.rs::test_simplified_purl_ordering_preserved` asserts `limit=2` returns 2
  items with `total == 3`.

## Caveat
When qualifier-variant duplicates exist, the in-memory dedup runs *after* `LIMIT`/`OFFSET`. A page can
then return fewer than `limit` items, and `total` overcounts (see Criterion 3). For data without such
duplicates, which is what the existing pagination tests cover, pagination behaves as before.

`test_simplified_purl_ordering_preserved` is also weaker than its name suggests. It never checks the
order of the returned items (no assertion compares `items[0]` with `items[1]` or with expected
versions), so it does not actually prove sorting is preserved.

## Conclusion
The existing pagination and sorting mechanics are kept, and the existing tests still pass. The
interaction with deduplication is a defect in the Criterion 3 implementation and is reported there.
