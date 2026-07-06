# Criterion 4: Existing pagination and sorting behavior is preserved

## Acceptance Criterion

> Existing pagination and sorting behavior is preserved

## Verdict: PASS

## Reasoning

### Pagination implementation

The pagination logic in `modules/fundamental/src/purl/service/mod.rs` is preserved in the PR:

```rust
let items = query
    .offset(offset.unwrap_or(0) as u64)
    ...
    .all(&self.db)
    .await?
```

The `.offset()` and `.limit()` parameters remain unchanged. The `PaginatedResults { items, total }` return shape is preserved.

### Total count

The total count computation has been modified but not removed. The PR changes the count query to:

```rust
let total = query.clone()
    .select_only()
    .column(purl::Column::Id)
    .group_by(purl::Column::Id)
    .count(&self.db).await?;
```

This adds grouping to avoid counting duplicates that would arise from the removed qualifier join. The total still reflects the correct number of distinct PURLs.

### Test evidence -- unchanged pagination test

The existing `test_recommend_purls_pagination` test is NOT in the diff, meaning it was not modified. This test (visible in the base-branch version) seeds 5 versioned PURLs and asserts:

```rust
// When requesting with limit=2
let resp = ctx.get("/api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3&limit=2").await;

// Then only 2 items are returned but total reflects all versions
assert_eq!(body.items.len(), 2);
assert_eq!(body.total, 5);
```

Since all CI checks pass (as stated in the task), this unchanged pagination test continues to pass, confirming pagination behavior is preserved.

### Test evidence -- new ordering test

The new `test_simplified_purl_ordering_preserved` test in `tests/api/purl_simplify.rs` verifies ordering with a limit parameter:

```rust
let resp = ctx.get("/api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3&limit=2").await;
assert_eq!(body.items.len(), 2);
assert_eq!(body.total, 3);
```

This confirms that pagination (limit) and total count work correctly after the qualifier removal changes.

This criterion is satisfied.
