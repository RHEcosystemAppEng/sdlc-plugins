# Criterion 1: Versioned PURLs without qualifiers

**Criterion:** `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

**Verdict:** PASS

## Reasoning

The code in `modules/fundamental/src/purl/service/mod.rs` demonstrates that the recommendation service now calls `p.without_qualifiers()` on each PURL result before serializing it:

```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

This strips all qualifier parameters from the PURL before including it in the response. The endpoint handler in `recommend.rs` still returns `Json<PaginatedResults<PurlSummary>>`, so the response shape is preserved while the content now contains versioned PURLs without qualifiers.

The test `test_recommend_purls_basic` explicitly validates this behavior:
```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This confirms the endpoint returns versioned PURLs (with `@3.12` version) without qualifier strings. All CI checks pass, which means this test assertion succeeds.
