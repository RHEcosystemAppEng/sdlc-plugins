# Criterion 3: Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

**Verdict: FAIL**

## Reasoning
The PR adds deduplication, but the way it is applied does not meet the criterion in general:

```rust
let items = query
    .offset(offset.unwrap_or(0) as u64)
    /* .limit(...) */
    .all(&self.db).await?
    .into_iter()
    .map(|p| { let simplified = p.without_qualifiers(); PurlSummary { purl: simplified.to_string() } })
    .dedup_by(|a, b| a.purl == b.purl)
    .collect();
```

1. **Only adjacent duplicates are removed.** `Itertools::dedup_by` drops runs of consecutive equal elements. It does not deduplicate the whole set.
2. **Nothing makes duplicates adjacent.** The query has no `order_by`/`ORDER BY`, and the diff does not add one. PostgreSQL gives no ordering guarantee without one. If the rows come back as `@3.12?repo1`, `@3.11?...`, `@3.12?repo2`, the response contains `pkg:maven/org.apache/commons-lang3@3.12` twice.
3. **Deduplication runs after OFFSET/LIMIT, on one page only.** Qualifier variants that fall on either side of a page boundary each appear on their own page, so the same simplified PURL is returned on two pages.
4. **`total` is not deduplicated.** `total` is now `select_only().column(Id).group_by(Id).count()`. With the join removed, `purl.id` is already unique, so the GROUP BY has no effect and `total` is the raw number of purl rows. In the scenario `test_recommend_purls_dedup` covers (two qualifier variants of `@3.12`), the response has `items.len() == 1` and `total == 2`. That is inconsistent.

## Test evidence
- `test_recommend_purls_dedup` seeds only two rows, which are adjacent anyway, and asserts `items.len() == 1` and the purl value. It never asserts `body.total`, and it does not cover interleaved versions or page boundaries. That is why CI passes even though the logic is wrong.

## Suggested fix (for the sub-task)
Deduplicate in SQL on the simplified identity (type/namespace/name/version) using `DISTINCT`/`GROUP BY` plus an explicit `ORDER BY`. Then apply OFFSET/LIMIT and COUNT to that deduplicated set. Add tests for interleaved variants, duplicates that cross a page boundary, and `total`.
