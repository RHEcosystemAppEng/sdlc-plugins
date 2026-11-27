# Criterion 3 — FAIL

**Criterion:** Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response.

## Reasoning

The PR adds deduplication, but only in a partial and order-dependent form:

```rust
let items = query
    .offset(offset.unwrap_or(0) as u64)
    .limit(...)
    .all(&self.db)
    .await?
    .into_iter()
    .map(|p| { ... without_qualifiers() ... })
    .dedup_by(|a, b| a.purl == b.purl)
    .collect();
```

1. **Only adjacent duplicates are removed.** `Itertools::dedup_by` (like `Vec::dedup_by`) only collapses runs of consecutive equal elements. The query has no `ORDER BY`, so PostgreSQL may return rows in any order. Rows that become the same PURL after simplification are not guaranteed to be next to each other. For example, the row order `@3.12?repo1`, `@3.11?...`, `@3.12?repo2` simplifies to `@3.12, @3.11, @3.12`, and all three entries survive.
2. **Dedup runs after SQL OFFSET/LIMIT.** It works only inside one page. If two qualifier variants of the same version fall on different pages, both pages return the same PURL, so the response as a whole is not deduplicated.
3. **`total` is not deduplicated.** `total` comes from `select_only().column(Id).group_by(Id).count()`, which counts raw `purl` rows. In the PR's own `test_recommend_purls_dedup` scenario, `items.len() == 1` but `total == 2`, so the response reports the count before dedup.

## Test gaps

- `test_recommend_purls_dedup` seeds two rows that are probably adjacent and asserts only `items.len() == 1`. It never asserts `total`, and it does not cover duplicates that are non-adjacent or that cross a page boundary.
- The test passes, but it does not show that the criterion holds in general.

## Fix needed

Deduplicate in SQL before pagination, using `DISTINCT` or `GROUP BY` on the version-level identity (type/namespace/name/version). Add a deterministic `ORDER BY`, and compute `total` over the same distinct set.
