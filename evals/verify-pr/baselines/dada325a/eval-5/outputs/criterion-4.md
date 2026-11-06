# Criterion 4

**Criterion:** Existing pagination and sorting behavior is preserved

**Verdict:** PASS (with advisory notes)

## What was checked

- **Pagination:** in `PurlService::recommend`, `.offset(offset.unwrap_or(0) as u64)` and the following limit call are unchanged by the diff. `total` is still computed and returned in `PaginatedResults { items, total }`. Its calculation changed from `query.clone().count()` to a `select_only().column(Id).group_by(Id).count()`. Now that the qualifier join is gone, this counts distinct purl rows. That matches the old count for data where each purl had at most one qualifier row, and it fixes inflation caused by the old LEFT JOIN when a row had several.
- **Sorting:** the diff adds and removes no `order_by` clauses. Ordering is left exactly as it was.
- **Regression coverage:** the base-branch test `test_recommend_purls_pagination` (5 versions, `limit=2`, asserts `items.len() == 2` and `total == 5`) is untouched by the diff. It still runs and CI passes. `test_recommend_purls_unknown_returns_empty` is also untouched and passing.
- The new `test_simplified_purl_ordering_preserved` asserts `limit=2` gives 2 items and `total == 3`.

## Notes

- Despite its name, `test_simplified_purl_ordering_preserved` asserts no ordering at all. It checks only item count, the absence of `?`, and `total`, so it adds pagination coverage but none for sorting.
- Because dedup runs after `offset`/`limit` (see criterion 3), pages can come back smaller than `limit` once duplicates exist. That is new behavior, but only for data that previously returned qualifier variants as separate rows. For data without duplicates, pagination behaves as before.
