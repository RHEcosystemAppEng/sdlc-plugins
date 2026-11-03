# Criterion 4 — PASS (with caveat)

**Criterion:** Existing pagination and sorting behavior is preserved.

## What was checked
- **Pagination parameters:** `offset.unwrap_or(0)` and `limit` are still applied to the query exactly as before. The endpoint signature and `RecommendParams` handling in recommend.rs are unchanged.
- **Total count:** `total` changed from `query.clone().count()` on the joined query to a count grouped by `purl::Column::Id`. Without duplicates, this gives the same per-purl count. Removing the qualifier join also stops the count from being inflated by joined qualifier rows.
- **Sorting:** the diff neither adds nor removes any `order_by`. The ordering the query had before (the database's default order on `Purl::find()` with the namespace/name filters) is unchanged.

## Test evidence
- `test_recommend_purls_pagination` (5 versions, `limit=2`, asserts `items.len() == 2` and `total == 5`) is **unchanged** by the PR and still passes in CI.
- `test_recommend_purls_unknown_returns_empty` (asserts `total == 0`) is unchanged and passes.
- The new `test_simplified_purl_ordering_preserved` asserts `items.len() == 2` and `total == 3` with `limit=2`.

## Caveat
- `test_simplified_purl_ordering_preserved` claims to check that ordering is preserved, but it never asserts the order of the items. It only checks the count, the absence of `?` and `total`. Sorting is therefore not actually tested.
- When duplicates exist, the per-page dedup described in criterion 3 means page sizes can shrink and `total` overcounts. That is a new scenario created by this change rather than a regression of existing behavior, so it is counted as a failure under criterion 3, not here.

**Verdict: PASS**
