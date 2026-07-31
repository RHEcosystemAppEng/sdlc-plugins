# Criterion 4: Pagination and sorting behavior preserved

## Acceptance Criterion

> Existing pagination and sorting behavior is preserved

## Verdict: PASS

## Analysis

### Implementation Evidence

The pagination parameters (`offset` and `limit`) are preserved in the service code. The query still uses:

```rust
.offset(offset.unwrap_or(0) as u64)
```

and the limit parameter (visible in the unchanged portion of the diff). These parameters control result pagination identically to the pre-change behavior.

### Total Count Query Change

The total count query was modified:

```rust
// Before:
let total = query.clone().count(&self.db).await?;

// After:
let total = query.clone()
    .select_only()
    .column(purl::Column::Id)
    .group_by(purl::Column::Id)
    .count(&self.db).await?;
```

The `group_by(purl::Column::Id)` groups by the primary key before counting. Since each row has a unique ID, this produces the same count as before. The `select_only().column(purl::Column::Id)` narrows the SELECT clause for efficiency but does not change the result set.

### Test Evidence

The existing `test_recommend_purls_pagination` test (visible in the base-branch file) is NOT modified in the PR diff, meaning it remains unchanged and continues to pass. This test:

1. Seeds 5 versioned PURLs
2. Requests with `limit=2`
3. Asserts `body.items.len() == 2` (pagination applied)
4. Asserts `body.total == 5` (total reflects all items)

The new `test_simplified_purl_ordering_preserved` test in `tests/api/purl_simplify.rs` also validates pagination and ordering:

1. Seeds 3 versions with qualifiers
2. Requests with `limit=2`
3. Asserts `body.items.len() == 2` and `body.total == 3`
4. Asserts no qualifiers in the paginated results

### CI Evidence

All CI checks pass, which includes the unchanged pagination test.

### Conclusion

Pagination and sorting behavior is preserved. The offset/limit parameters are unchanged in the service code, the total count query produces equivalent results, and both existing and new tests validate pagination works correctly with the simplified response format.
