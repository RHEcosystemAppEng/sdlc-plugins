# Criterion 3: Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

**Verdict: FAIL**

## Code inspected
`modules/fundamental/src/purl/service/mod.rs`:

```rust
let items = query
    .offset(offset.unwrap_or(0) as u64)
    // .limit(...)
    .all(&self.db)
    .await?
    .into_iter()
    .map(|p| { let simplified = p.without_qualifiers(); PurlSummary { purl: simplified.to_string() } })
    .dedup_by(|a, b| a.purl == b.purl)
    .collect();
```

## Findings
1. **Only adjacent duplicates are removed.**
   - `Itertools::dedup_by` drops only *consecutive* equal elements, the same as `Vec::dedup_by`. It does not deduplicate the whole result set.
   - The query is `Purl::find().filter(namespace).filter(name)` with no `.order_by(...)` in the diff or the visible context.
   - Without ORDER BY, PostgreSQL does not guarantee row order. Rows `3.12?repo1`, `3.11?...`, `3.12?repo2` can come back interleaved. After simplification they become `[3.12, 3.11, 3.12]`, and the duplicate survives.
2. **Dedup runs after pagination.**
   - Offset and limit run in SQL. Dedup then runs in Rust on that single page.
   - Qualifier variants that fall on either side of a page boundary are never merged, so the same PURL shows up on two pages.
3. **`total` is not deduplicated.**
   - `total` is computed as `query.select_only().column(Id).group_by(Id).count()`. That counts distinct purl *rows*. Grouping by the primary key does nothing now that the join is gone.
   - In the dedup scenario with two rows, `items.len() == 1` but `total == 2`.

## Tests
- `test_recommend_purls_dedup` was added, as the Test Requirements ask. It seeds exactly two rows that differ only by qualifier and contains nothing else. Those rows are trivially adjacent and fit in one page, so the test passes.
- No test covers interleaved, non-adjacent duplicates.
- No test covers duplicates across a page boundary.
- `body.total` is never asserted in the dedup test.

## Assessment
Deduplication works only in the trivial case the single test exercises. The criterion asks for duplicates to be removed from the response, and the implementation does not guarantee that in general. A sub-task is proposed: deduplicate in SQL (DISTINCT on the simplified identity) with a deterministic ORDER BY before offset/limit, compute `total` over the same distinct set, and add tests for interleaved and cross-page duplicates and for `total`.
