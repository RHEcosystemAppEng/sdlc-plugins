## Criterion 4: Existing pagination and sorting behavior is preserved

**Criterion:** Existing pagination and sorting behavior is preserved

**Verdict:** PASS

### Reasoning

**Pagination implementation preserved:**

In `modules/fundamental/src/purl/service/mod.rs`, the query pipeline retains its pagination logic:

```rust
let items = query
    .offset(offset.unwrap_or(0) as u64)
    ...
    .all(&self.db)
    .await?
```

The `.offset()` and `.limit()` calls remain unchanged from the base branch. The dedup and qualifier stripping happen after the database query returns results, so they do not affect the SQL-level pagination.

**Total count adjustment:**

The total count query was modified to use `select_only()`, `column()`, and `group_by()`:

```rust
let total = query.clone()
    .select_only()
    .column(purl::Column::Id)
    .group_by(purl::Column::Id)
    .count(&self.db).await?;
```

This change accounts for the removed qualifier join -- without the join, the count no longer needs deduplication at the SQL level. The `group_by` ensures accurate counting when rows might be duplicated by other query conditions.

**Test verification:**

1. The existing `test_recommend_purls_pagination` test is preserved unchanged in the PR. It seeds 5 versioned PURLs, requests with `limit=2`, and asserts `body.items.len() == 2` and `body.total == 5`. This test continues to verify pagination behavior.

2. The new `test_simplified_purl_ordering_preserved` in `tests/api/purl_simplify.rs` explicitly tests ordering and pagination together:
   - Seeds 3 versioned PURLs with qualifiers
   - Requests with `limit=2`
   - Asserts `body.items.len() == 2` and `body.total == 3`
   - Confirms ordering is preserved after qualifier removal

**Conclusion:** The pagination and sorting query logic is preserved, the existing pagination test remains unchanged, and a new test explicitly verifies ordering is maintained. The criterion is satisfied.
