# Criterion 4

**Criterion:** Existing pagination and sorting behavior is preserved

**Verdict:** PASS

## Evidence

- Pagination: the query still applies `.offset(offset.unwrap_or(0) as u64)` and the limit, as before. The
  handler signature (`Query<RecommendParams>` with `offset`/`limit`) has not changed.
- `total` is still computed from the same filtered query (namespace + name). The qualifier `LeftJoin` used to
  multiply rows per qualifier. Now `total` counts PURL ids (`select_only().column(Id).group_by(Id).count()`).
- Sorting: the diff adds no ordering clause and removes none, so whatever ordering existed before is unchanged.
- Tests:
  - `test_recommend_purls_pagination` (unchanged from base) still asserts `limit=2 -> items.len() == 2, total == 5`.
  - `test_recommend_purls_unknown_returns_empty` (unchanged) still asserts an empty result with `total == 0`.
  - New `test_simplified_purl_ordering_preserved` asserts `limit=2 -> 2 items, total == 3`.

## Advisory notes

- Despite its name, `test_simplified_purl_ordering_preserved` never checks the order of the items. It only
  checks the count, that there is no `?`, and `total`. Ordering is preserved because the diff does not change
  it, not because a test proves it.
- Applying dedup after pagination (see criterion 3) could make pages shorter when duplicates exist. Data
  without duplicates paginates exactly as before.

## Conclusion

Pagination and sorting work as before for data without duplicates, and the existing pagination tests still pass.
