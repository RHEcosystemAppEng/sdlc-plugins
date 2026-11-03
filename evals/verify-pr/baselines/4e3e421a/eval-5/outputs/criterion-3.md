# Criterion 3 — FAIL

**Criterion:** Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response.

## What was checked
Dedup is implemented in `PurlService::recommend` (modules/fundamental/src/purl/service/mod.rs):

```rust
let items = query
    .offset(offset.unwrap_or(0) as u64)
    .limit(...)
    .all(&self.db)
    .await?
    .into_iter()
    .map(|p| { let simplified = p.without_qualifiers(); PurlSummary { purl: simplified.to_string() } })
    .dedup_by(|a, b| a.purl == b.purl)
    .collect();
```

The approach has three defects. Each one means duplicates are not reliably removed from the response:

1. **Only consecutive duplicates are removed.** `dedup_by` (Itertools) drops only *adjacent* equal elements. The query has no `ORDER BY`, so the database does not have to return two rows that become equal after stripping qualifiers next to each other. For example, `@3.12?repo1`, `@3.11?...`, `@3.12?repo2` would still return `@3.12` twice.
2. **Dedup runs after pagination.** `offset`/`limit` are applied in SQL to the raw, non-deduplicated rows. Dedup then runs only inside one page:
   - Duplicates that fall on different pages are never merged, so the same PURL can appear on page 1 and on page 2.
   - A page asked for with `limit=N` can return fewer than N items even when more unique items exist.
3. **`total` is not deduplicated.** `total` is computed as `select_only().column(purl::Column::Id).group_by(purl::Column::Id).count()`. That counts distinct purl *rows*, not distinct qualifier-stripped PURLs. In the dedup scenario (two rows that differ only by qualifier), `total` = 2 while `items.len()` = 1, so the response contradicts itself.

## Test evidence
- `test_recommend_purls_dedup` seeds two PURLs that differ only in `repository_url` and asserts `items.len() == 1`. The test passes only because there are just two rows, both on one page, so they happen to be adjacent. It does **not** assert `body.total`, so the `total` mismatch goes unnoticed. It also never puts a different version between the duplicates or spreads them across pages.
- No test covers non-adjacent duplicates or duplicates across pages.

## Required fix (recommendation)
Deduplicate in the query: `SELECT DISTINCT` on the qualifier-stripped identity (namespace, name, version), or group by those columns. Apply the same distinct/group-by to both the `count` and the paged `items` query, and add a deterministic `ORDER BY`, so that pagination and `total` work on deduplicated rows. Extend `test_recommend_purls_dedup` to assert `total == 1` and add a case where the duplicates are not adjacent.

**Verdict: FAIL** (dedup is partial: it relies on row adjacency, covers only the current page, and leaves `total` inconsistent with the items)
