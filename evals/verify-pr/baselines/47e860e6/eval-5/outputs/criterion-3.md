# Criterion 3: Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

**Verdict: FAIL**

## Implementation
```rust
let items = query
    .offset(offset.unwrap_or(0) as u64)
    .limit(...)
    .all(&self.db).await?
    .into_iter()
    .map(|p| { let simplified = p.without_qualifiers(); PurlSummary { purl: simplified.to_string() } })
    .dedup_by(|a, b| a.purl == b.purl)
    .collect();
```

## Problems
1. **Only adjacent duplicates are removed.** `dedup_by` (Itertools / `Vec::dedup_by`) removes *consecutive* equal items only. The query has no `ORDER BY`, so PostgreSQL can return rows in any order.
   - Example: rows `3.12?repo1`, `3.11`, `3.12?repo2` simplify to `[3.12, 3.11, 3.12]`. `dedup_by` leaves this unchanged, so the response still contains a duplicate.
   - Sorting by `id` would not fix this. Duplicates need to be grouped by the qualifier-free identity, or removed with `DISTINCT` / `GROUP BY` or a set.
2. **Dedup runs after pagination.** `.offset()` / `.limit()` are applied in SQL before the in-memory dedup, so dedup only sees one page.
   - Example: with `limit=2`, `3.12?repo1` can be on page 1 and `3.12?repo2` on page 2. The same simplified PURL then appears on both pages.
3. **`total` is not deduplicated.** `total` is `select_only().column(Id).group_by(Id).count()`. With the join gone, that is just the number of raw purl rows. In the dedup test's own scenario, `items.len() == 1` but `total == 2`.

## Test weakness
`test_recommend_purls_dedup` seeds exactly two rows for the same version. Two rows are always adjacent and fit on one page, so the test passes even with adjacent-only, per-page dedup. It does not assert `body.total`. No test covers:
- non-adjacent duplicates
- duplicates mixed with other versions
- duplicates across a page boundary

## Conclusion
Dedup works only in the narrow case the test covers. The criterion is not reliably met.
