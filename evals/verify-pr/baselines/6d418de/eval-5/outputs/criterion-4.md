# Criterion 4: Existing pagination and sorting behavior is preserved

## Verdict: FAIL

## Reasoning

There are two issues affecting pagination behavior:

### Issue 1: `total` count reflects pre-dedup count

The `total` field in `PaginatedResults` is computed from a database query before Rust-side deduplication occurs:

```rust
let total = query.clone()
    .select_only()
    .column(purl::Column::Id)
    .group_by(purl::Column::Id)
    .count(&self.db).await?;
```

Since `purl::Column::Id` is unique per row, `GROUP BY id` followed by `COUNT` is equivalent to counting all matching rows. This count does NOT account for deduplication that happens after `without_qualifiers()` in Rust. When duplicates exist (entries that differ only by qualifiers), `total` will be higher than the actual number of unique results returned in `items`.

For example, if 2 purl rows with different qualifiers match the query, `total` would be 2 but `items` after dedup would contain 1. Clients relying on `total` to compute page counts would see incorrect values (e.g., expecting a second page when all results fit on one page).

The test `test_recommend_purls_dedup` asserts `body.items.len() == 1` but does NOT assert `body.total`, so this mismatch is not caught by tests.

### Issue 2: Pagination/dedup interaction

The deduplication happens AFTER pagination (`offset`/`limit`) is applied at the database level. This means:
1. The database returns `limit` rows (including potential duplicates)
2. Rust strips qualifiers and deduplicates
3. The final `items` may have fewer entries than `limit`

This breaks the pagination contract where clients expect exactly `limit` items (or fewer only on the last page).

### Preserved behaviors

The `offset` and `limit` parameters still work at the query level. The `test_simplified_purl_ordering_preserved` test uses `limit=2` and verifies 2 items are returned with `total == 3` (no duplicates in this test case). The existing `test_recommend_purls_pagination` test is unchanged but would also be affected by this issue if any seeded PURLs became duplicates after qualifier stripping.

## Evidence

- `modules/fundamental/src/purl/service/mod.rs`: `total` computed from query; dedup applied in Rust after `.all()` and `.map()`
- `tests/api/purl_recommend.rs`: `test_recommend_purls_dedup` does not assert `body.total`
- Pagination applies at DB level (`.offset()`, `.limit()`), dedup at Rust level (`.dedup_by()`) — ordering mismatch
