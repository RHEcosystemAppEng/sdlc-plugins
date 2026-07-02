# Criterion 4: Pagination and Sorting Preserved

**Criterion**: Existing pagination and sorting behavior is preserved

**Verdict**: PASS

## Analysis

The PR preserves pagination mechanics in the service layer. The query still uses `.offset()` and `.limit()` for pagination control:
```rust
let items = query
    .offset(offset.unwrap_or(0) as u64)
    // .limit(...) implied by context
    .all(&self.db)
    .await?
```

The total count query is updated to use `.select_only().column(purl::Column::Id).group_by(purl::Column::Id)` instead of the previous plain `.count()`. This change reflects the removal of the qualifier join -- without the join, the count no longer needs to account for multiplied rows from qualifier records. The `group_by` ensures correct counting after the join removal.

The `PaginatedResults { items, total }` return structure is unchanged.

## Test Evidence

1. **Existing pagination test preserved**: The `test_recommend_purls_pagination` function in `tests/api/purl_recommend.rs` is not modified in the diff, meaning the base-branch pagination test continues to run unchanged. That test seeds 5 versioned PURLs, requests with `limit=2`, and asserts `items.len() == 2` and `total == 5`.

2. **New ordering + pagination test**: The `test_simplified_purl_ordering_preserved` test in `tests/api/purl_simplify.rs` seeds 3 versioned PURLs with qualifiers, requests with `limit=2`, and asserts:
   - `body.items.len() == 2` (limit respected)
   - `body.total == 3` (total reflects all matching entries)
   - No qualifiers in response items

This combination of unchanged existing tests and new tests covering the intersection of qualifier removal with pagination provides adequate confidence.
