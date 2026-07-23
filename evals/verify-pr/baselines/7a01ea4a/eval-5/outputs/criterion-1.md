## Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

**Verdict: PASS**

### Analysis

The acceptance criterion requires that `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers (e.g., `pkg:maven/org.apache/commons-lang3@3.12` instead of `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar`).

### Evidence from the PR Diff

**Service layer change (`modules/fundamental/src/purl/service/mod.rs`):**

The service code now calls `p.without_qualifiers()` before serializing the PURL:

```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

Previously, the code serialized the full PURL including qualifiers:

```rust
.map(|p| PurlSummary {
    purl: p.to_string(),
})
```

This change strips qualifier information from every PURL in the response. The `without_qualifiers()` method is documented in the task's Implementation Notes as being available on the `PackageUrl` builder in `common/src/purl.rs`.

**Endpoint layer change (`modules/fundamental/src/purl/endpoints/recommend.rs`):**

The `JoinType` import was removed since the qualifier join is no longer needed. The endpoint's return type remains `Result<Json<PaginatedResults<PurlSummary>>, AppError>`, preserving the response shape.

**Test verification (`tests/api/purl_recommend.rs`):**

The `test_recommend_purls_basic` test now asserts that the returned PURL matches the versioned-only format:

```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

Previously, it asserted the fully qualified format:

```rust
assert_eq!(
    body.items[0].purl,
    "pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar"
);
```

### Conclusion

The service layer correctly strips qualifiers using the `without_qualifiers()` method, and the test verifies the expected versioned-only format. This criterion is satisfied.
