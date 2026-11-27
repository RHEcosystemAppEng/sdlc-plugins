# Criterion 4 — FAIL

**Criterion:** Existing pagination and sorting behavior is preserved.

## Reasoning

- **Pages can now come back short.** Dedup runs in Rust after SQL `OFFSET`/`LIMIT`, so a page can hold fewer than `limit` items even when more distinct results exist. For example, with `limit=2` and the rows `@3.12?repo1`, `@3.12?repo2`, `@3.11`, the page returns one item although `@3.11` exists. A client that pages with `offset += limit` will see short pages and duplicates across pages.
- **`total` no longer matches `items`.** `total` counts raw `purl.id` rows (`group_by(purl::Column::Id).count()`), while `items` is deduplicated. A client that derives a page count from `total` will compute too many pages. Before this PR, `total` and `items` were computed over the same row set. The semantics also changed without documentation: the old count ran over the LEFT JOIN with `purl_qualifier`, and the new one runs on bare `purl` rows grouped by id.
- **Sorting is not guaranteed.** Neither the base query nor the new one has an `ORDER BY`. Removing the join can change the physical order of the rows PostgreSQL returns, and correct adjacent-only dedup would need a deterministic order anyway.
- **The "ordering preserved" test does not check order.** `test_simplified_purl_ordering_preserved` asserts only `len == 2`, the absence of `?`, and `total == 3`. Its name and doc comment claim more than it verifies.
- **The existing pagination test does not cover duplicates.** The unchanged base test `test_recommend_purls_pagination` (5 distinct versions, `limit=2`, `total == 5`) passes only because it has no duplicates. It never exercises dedup together with pagination.

## Verdict

FAIL. Pagination stays correct only when no qualifier duplicates exist. Duplicates are the exact case this task introduces, and in that case `total` and page sizes are wrong. Preservation of sort order is not demonstrated either.
