# Criterion 1 Analysis

**Criterion:** `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

**Verdict:** PASS

## Evidence

### Code Changes

In `modules/fundamental/src/purl/service/mod.rs`, the recommendation mapping was changed from returning the raw PURL string to stripping qualifiers first:

**Before (base branch):**
```rust
.map(|p| PurlSummary {
    purl: p.to_string(),
})
```

**After (PR branch):**
```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

The `without_qualifiers()` method (documented in the task as available on `PackageUrl` builder in `common/src/purl.rs`) strips all qualifier key-value pairs from the PURL, leaving only the scheme, type, namespace, name, and version components. This means a PURL like `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar` becomes `pkg:maven/org.apache/commons-lang3@3.12`.

### Endpoint Preservation

The endpoint handler in `modules/fundamental/src/purl/endpoints/recommend.rs` still serves `GET /api/v2/purl/recommend` with the same `RecommendParams` query extraction (including `purl` parameter). The route and parameter handling are unchanged -- only the service layer response content changed.

### Test Verification

In `tests/api/purl_recommend.rs`, the `test_recommend_purls_basic` test seeds PURLs with qualifiers and then asserts that the response contains versioned PURLs without qualifiers:

```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This confirms the endpoint returns versioned PURLs (includes `@3.12`) without qualifiers (no `?` or key-value pairs after the version).

### Additional Test Coverage

The new `tests/api/purl_simplify.rs` file includes `test_simplified_purl_mixed_types` which verifies the behavior across different PURL types (npm, pypi), confirming the qualifier stripping is not limited to Maven PURLs:

```rust
assert_eq!(body.items[0].purl, "pkg:npm/%40angular/core@16.0.0");
assert!(!body.items[0].purl.contains("vcs_url"));
```

## Conclusion

The code change correctly implements qualifier removal at the service layer via `without_qualifiers()`, the endpoint route and parameters are preserved, and multiple tests verify the expected output format. Criterion is satisfied.
