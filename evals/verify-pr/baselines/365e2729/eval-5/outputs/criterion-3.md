# Criterion 3: Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

**Verdict: FAIL**

## What was checked
The PR adds deduplication in `PurlService::recommend` (`modules/fundamental/src/purl/service/mod.rs`):

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

There are three problems with this.

1. **It only removes adjacent duplicates, and the order is not fixed.** `Itertools::dedup_by` drops
   duplicates only when they sit next to each other. The query has no `ORDER BY`: the diff adds none,
   and none is visible in the context lines. So rows that become the same PURL once qualifiers are
   stripped are not guaranteed to be adjacent. Example: rows ordered
   `3.12?repo1`, `3.11?repo1`, `3.12?repo2` come out as `3.12`, `3.11`, `3.12`, so the duplicate stays.
2. **It runs after pagination.** `offset`/`limit` are applied in SQL before the dedup, which happens in
   memory on a single page. Duplicates that span a page boundary are not removed. A page can also hold
   fewer than `limit` items even when more distinct results exist.
3. **`total` is not deduplicated.** `total` is now computed as
   `select_only().column(purl::Column::Id).group_by(purl::Column::Id).count()`. This counts distinct
   purl *rows*, not distinct *simplified* PURLs. In the scenario the new dedup test seeds (the same
   version with two `repository_url` qualifiers, stored as two purl rows), `items.len()` is 1 but
   `total` is 2. The response contradicts itself.

## Test evidence
- `test_recommend_purls_dedup` seeds exactly two rows that differ only in qualifiers and asserts
  `items.len() == 1` and `items[0].purl == "pkg:maven/org.apache/commons-lang3@3.12"`. Two rows will
  almost certainly come back adjacent, so the test passes (CI is green). It does not cover
  non-adjacent duplicates or duplicates across pages, and it does not assert `body.total`, so it
  cannot catch any of the three problems above.

## Conclusion
Deduplication works only for the narrow case the test seeds. The response as a whole (items across
pages, plus `total`) is not reliably deduplicated, so the criterion is not met.

**Suggested fix:** deduplicate in the database before pagination. One way is to select
`DISTINCT` on the qualifier-free columns (type/namespace/name/version), with a deterministic
`ORDER BY`, and compute `total` from the same distinct projection. Then add a test that asserts
`total` and covers non-adjacent duplicates.
