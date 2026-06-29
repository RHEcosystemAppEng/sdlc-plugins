# Criterion 1: `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

## Verdict: PASS

## Reasoning

The PR modifies the service layer in `modules/fundamental/src/purl/service/mod.rs` to strip qualifiers from PURLs before constructing the response. Specifically, the change replaces:

```rust
.map(|p| PurlSummary {
    purl: p.to_string(),
})
```

with:

```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

The `without_qualifiers()` method (documented in the task as existing in `common/src/purl.rs`) constructs a PURL without qualifier components. The resulting string will be a versioned PURL like `pkg:maven/org.apache/commons-lang3@3.12` instead of `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar`.

The test `test_recommend_purls_basic` in `tests/api/purl_recommend.rs` explicitly verifies this:
```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This assertion confirms the endpoint returns versioned PURLs (with `@3.12`) without qualifiers (no `?` or anything after it).

Additionally, the new test file `tests/api/purl_simplify.rs` contains `test_simplified_purl_no_version` which verifies the edge case where PURLs have no version, and `test_simplified_purl_mixed_types` which verifies the behavior across different PURL types (npm, pypi).

## Evidence

- `modules/fundamental/src/purl/service/mod.rs`: `p.without_qualifiers()` call strips qualifiers
- `tests/api/purl_recommend.rs`: `assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12")` confirms versioned PURL without qualifiers
- `tests/api/purl_simplify.rs`: Multiple tests confirm simplified format across different PURL types
