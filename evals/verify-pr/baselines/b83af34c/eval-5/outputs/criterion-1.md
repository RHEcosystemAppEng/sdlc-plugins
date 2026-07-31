# Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

## Acceptance Criterion

> `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

## Verdict: PASS

## Analysis

### Implementation Evidence

The PR modifies the PURL recommendation service in `modules/fundamental/src/purl/service/mod.rs` to strip qualifiers from returned PURLs. The key change is:

```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

Previously, the code returned the full PURL string including qualifiers:

```rust
.map(|p| PurlSummary {
    purl: p.to_string(),
})
```

The `without_qualifiers()` method (documented in the task as available on `PackageUrl` builder in `common/src/purl.rs`) constructs a PURL retaining only the type, namespace, name, and version components -- stripping any query parameters (qualifiers).

### Endpoint Evidence

The endpoint in `modules/fundamental/src/purl/endpoints/recommend.rs` continues to accept the same query parameter `purl` and returns the same response type. The qualifier removal happens at the service layer, ensuring the endpoint contract is preserved.

### Test Evidence

The test `test_recommend_purls_basic` in `tests/api/purl_recommend.rs` was updated to verify this behavior:

- Seeds PURLs with qualifiers: `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar`
- Asserts the response contains versioned PURLs without qualifiers: `assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12")`

The seeded PURLs include qualifiers but the assertion expects only the versioned PURL, confirming the endpoint strips qualifiers from the response.

### Conclusion

The implementation correctly returns versioned PURLs without qualifiers. The service layer applies `without_qualifiers()` to each PURL before constructing the response summary, and the test confirms the expected output format.
