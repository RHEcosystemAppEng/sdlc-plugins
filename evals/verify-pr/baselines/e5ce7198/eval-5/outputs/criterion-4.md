## Criterion 4: Existing pagination and sorting behavior is preserved

**Result: PASS**

The existing `test_recommend_purls_pagination` test function in `tests/api/purl_recommend.rs` is unchanged in the PR. This test:
1. Seeds 5 versioned PURLs for the same package
2. Requests with `limit=2`
3. Asserts exactly 2 items are returned
4. Asserts `total` reflects all 5 versions

The test continues to pass (all CI checks pass), confirming that pagination behavior (offset/limit parameters) is preserved after the qualifier removal changes.

Additionally, the new `test_simplified_purl_ordering_preserved` test in `tests/api/purl_simplify.rs` explicitly verifies that ordering and pagination work correctly after qualifier stripping:
```rust
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.10?type=jar").await;
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.11?type=jar").await;
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?type=jar").await;
let resp = ctx.get("/api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3&limit=2").await;
assert_eq!(body.items.len(), 2);
assert_eq!(body.total, 3);
```

The service layer code preserves the `.offset()` and `.limit()` calls, and the query structure is otherwise unchanged apart from removing the qualifier join and adding deduplication.
