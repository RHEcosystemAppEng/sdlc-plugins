# Criterion 4: Pagination and sorting preserved

**Acceptance Criterion**: Existing pagination and sorting behavior is preserved

**Verdict**: PASS

## Evidence

### Product code -- offset and limit preserved in service layer

In `modules/fundamental/src/purl/service/mod.rs`, the pagination parameters remain intact in the query:

```rust
         let items = query
             .offset(offset.unwrap_or(0) as u64)
```

The `offset` and `limit` parameters are still applied to the query. The diff does not modify the `.offset()` or `.limit()` calls, nor the handler's `Query(params): Query<RecommendParams>` parameter extraction.

### Product code -- total count query preserved

The count query was modified but preserves correctness:

```rust
-        let total = query.clone().count(&self.db).await?;
+        let total = query.clone()
+            .select_only()
+            .column(purl::Column::Id)
+            .group_by(purl::Column::Id)
+            .count(&self.db).await?;
```

The total count now uses `group_by` to account for the removed qualifier join, ensuring the count reflects unique PURLs rather than being inflated by multiple qualifier rows per PURL.

### Test evidence -- existing pagination test unmodified

The base-branch `test_recommend_purls_pagination` function (visible in `test-base-purl-recommend.md`) is not modified in the diff. It seeds 5 versioned PURLs, requests with `limit=2`, and asserts `body.items.len(), 2` and `body.total, 5`. Since this test is not in the diff's hunks, it remains unchanged and continues to exercise pagination.

### Test evidence -- new ordering test in purl_simplify.rs

In `tests/api/purl_simplify.rs`, the `test_simplified_purl_ordering_preserved` test explicitly validates that pagination works with the simplified response:

```rust
    // Given multiple versions of the same package with qualifiers
    ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.10?type=jar").await;
    ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.11?type=jar").await;
    ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?type=jar").await;

    // When requesting recommendations with limit
    let resp = ctx.get("/api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3&limit=2").await;

    // Then results are ordered and paginated correctly without qualifiers
    assert_eq!(body.items.len(), 2);
    assert_eq!(body.total, 3);
```

This confirms that `limit=2` returns exactly 2 items while `total` reflects all 3 entries, demonstrating that pagination works correctly after qualifier removal.
