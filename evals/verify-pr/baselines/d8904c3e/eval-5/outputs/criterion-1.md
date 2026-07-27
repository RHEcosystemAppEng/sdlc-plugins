## Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

**Criterion:** `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

**Verdict:** PASS

### Reasoning

The PR makes two coordinated changes that satisfy this criterion:

**Service layer change (`modules/fundamental/src/purl/service/mod.rs`):**

The recommendation query pipeline now strips qualifiers before constructing the response. The key change is in the `.map()` closure:

```rust
// Before (base branch):
.map(|p| PurlSummary {
    purl: p.to_string(),
})

// After (PR branch):
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

The `without_qualifiers()` method (documented in the task as available on the `PackageUrl` builder in `common/src/purl.rs`) strips all qualifier key-value pairs, producing a versioned PURL like `pkg:maven/org.apache/commons-lang3@3.12` instead of the fully qualified form.

**Endpoint layer change (`modules/fundamental/src/purl/endpoints/recommend.rs`):**

The `JoinType` import was removed since the qualifier join is no longer needed. The endpoint return type remains `Result<Json<PaginatedResults<PurlSummary>>, AppError>`, confirming the response still flows through the same serialization path.

**Test verification (`tests/api/purl_recommend.rs`):**

The `test_recommend_purls_basic` test now asserts:
```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This confirms the endpoint returns the versioned PURL without qualifiers for the given input.

**Conclusion:** The service layer applies `without_qualifiers()` to every PURL before serialization, and the test asserts the expected versioned-only format. The criterion is satisfied.
