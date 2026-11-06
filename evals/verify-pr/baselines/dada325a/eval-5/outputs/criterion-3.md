# Criterion 3

**Criterion:** Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

**Verdict:** PASS (with robustness concerns, advisory)

## What was checked

`modules/fundamental/src/purl/service/mod.rs` adds a dedup step after the qualifiers are stripped:

```rust
.map(|p| { let simplified = p.without_qualifiers(); PurlSummary { purl: simplified.to_string() } })
.dedup_by(|a, b| a.purl == b.purl)
.collect();
```

Items whose simplified PURL strings are equal get collapsed. The new test `test_recommend_purls_dedup` seeds
`pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar` and
`...@3.12?repository_url=https://repo2.maven.org&type=jar`. It asserts `items.len() == 1` and
`items[0].purl == "pkg:maven/org.apache/commons-lang3@3.12"`. This is the exact scenario the criterion describes, and CI passes.

## Concerns (do not block the criterion, but worth a reviewer's look)

1. **Only adjacent duplicates are removed.** `dedup_by` (itertools, or `Vec::dedup_by`) collapses only consecutive equal elements. The query has no `ORDER BY`, so Postgres does not guarantee that rows with the same namespace/name/version come back next to each other. Example: if `@3.12?repo1`, `@3.11`, `@3.12?repo2` are returned in that order, the duplicate survives. The test only seeds two rows, so it never covers the non-adjacent case. A fix would be to order by version before deduplicating, or to dedup with a `HashSet`/`unique_by`, or with `DISTINCT` in SQL.
2. **Dedup happens after pagination.** `offset`/`limit` are applied in SQL before the dedup, so a page can hold fewer than `limit` items even when more distinct results exist.
3. **`total` does not match the deduplicated items.** `total` counts distinct `purl.id` rows (`group_by(purl::Column::Id)`), not distinct simplified PURLs. In the dedup scenario `items.len()` would be 1 while `total` could still be 2. `test_recommend_purls_dedup` does not assert `total`, so this goes untested.

The behavior the criterion asks for is implemented and tested for its stated scenario, so it is marked PASS. These gaps make the dedup unreliable on larger or unordered result sets.
