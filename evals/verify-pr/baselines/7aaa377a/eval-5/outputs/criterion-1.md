# Criterion 1: `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

## Verdict: PASS

## Analysis

This criterion requires that the recommendation endpoint returns versioned PURLs (e.g., `pkg:maven/org.apache/commons-lang3@3.12`) but without qualifier query parameters (no `?repository_url=...&type=jar`).

### Evidence from the PR diff

**Service layer change (`modules/fundamental/src/purl/service/mod.rs`):**

The service now calls `p.without_qualifiers()` before converting to string:

```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

Previously, the PURL was serialized directly with qualifiers:

```rust
.map(|p| PurlSummary {
    purl: p.to_string(),
})
```

The `without_qualifiers()` method is documented in the task's Implementation Notes as being available on the `PackageUrl` builder in `common/src/purl.rs`. This method strips qualifier parameters while preserving the type, namespace, name, and version components.

**Endpoint layer change (`modules/fundamental/src/purl/endpoints/recommend.rs`):**

The `JoinType` import for `sea_orm::JoinType` was removed, consistent with the service layer no longer joining the qualifier table. The return type remains `Result<Json<PaginatedResults<PurlSummary>>, AppError>`, confirming the response structure is unchanged.

**Test verification (`tests/api/purl_recommend.rs`):**

The `test_recommend_purls_basic` test now asserts:

```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This directly validates that the endpoint returns a versioned PURL (`@3.12`) without qualifiers. The old assertion checked for the fully qualified PURL including `?repository_url=https://repo1.maven.org&type=jar`.

**Additional test coverage (`tests/api/purl_simplify.rs`):**

The new `test_simplified_purl_no_version` test verifies PURLs without a version component also work correctly. The `test_simplified_purl_mixed_types` test verifies that different PURL types (npm, pypi) also have qualifiers stripped:

```rust
assert_eq!(body.items[0].purl, "pkg:npm/%40angular/core@16.0.0");
assert!(!body.items[0].purl.contains("vcs_url"));
```

### Conclusion

The code change directly implements the required behavior: the `without_qualifiers()` call in the service layer ensures all PURLs returned by the recommendation endpoint are versioned but lack qualifier parameters. Both modified and new tests validate this behavior.
