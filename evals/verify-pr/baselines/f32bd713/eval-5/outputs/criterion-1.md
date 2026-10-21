# Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

**Criterion:** `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

**Verdict:** PASS

## Reasoning

The PR modifies the PURL recommendation pipeline at two levels to strip qualifiers from the response:

### Service Layer Change (`modules/fundamental/src/purl/service/mod.rs`)

The service layer now transforms each PURL result through `without_qualifiers()` before serialization:

```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

Previously, the PURL was serialized directly via `p.to_string()`, which included all qualifiers. The `without_qualifiers()` method (documented in the task as available on `PackageUrl` in `common/src/purl.rs`) strips the qualifier portion, producing versioned PURLs like `pkg:maven/org.apache/commons-lang3@3.12` instead of `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar`.

### Endpoint Layer Change (`modules/fundamental/src/purl/endpoints/recommend.rs`)

The `JoinType` import was removed since the qualifier join is no longer needed. The endpoint signature and return type remain unchanged -- it still returns `Result<Json<PaginatedResults<PurlSummary>>, AppError>`.

### Test Verification

The updated `test_recommend_purls_basic` test directly asserts this behavior:

```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This confirms the endpoint returns a versioned PURL without qualifiers for the same seed data that previously returned the fully qualified version. The new test file `tests/api/purl_simplify.rs` further validates this for multiple PURL types (Maven, npm, pypi).

### Conclusion

The code changes demonstrate that the endpoint returns versioned PURLs without qualifiers. The service layer transformation is applied to every result, and the test assertions confirm the expected format. This criterion is satisfied.
