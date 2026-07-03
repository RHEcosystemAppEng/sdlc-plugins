## Criterion 1: `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

**Verdict: PASS**

### Analysis

The PR modifies the service layer in `modules/fundamental/src/purl/service/mod.rs` to strip qualifiers from PURLs before returning them. Specifically, the mapping logic changed from:

```rust
.map(|p| PurlSummary {
    purl: p.to_string(),
})
```

to:

```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

This calls `without_qualifiers()` on each PURL entity before serializing it, which strips all query parameters (qualifiers) from the PURL string while preserving the scheme, type, namespace, name, and version components.

The test `test_recommend_purls_basic` in `tests/api/purl_recommend.rs` was updated to verify this behavior. It seeds PURLs with qualifiers (`?repository_url=...&type=jar`) but asserts the response contains versioned PURLs without qualifiers:

```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This directly confirms that the endpoint returns versioned PURLs without qualifiers.

Additionally, the new test file `tests/api/purl_simplify.rs` includes `test_simplified_purl_mixed_types` which verifies the behavior for npm-type PURLs, confirming the qualifier removal is not limited to Maven PURLs.

CI passes, confirming these assertions hold at runtime.
