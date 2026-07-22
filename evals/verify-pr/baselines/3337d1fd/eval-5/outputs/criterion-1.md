# Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

## Verdict: PASS

## Analysis

This criterion requires that the `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` endpoint returns versioned PURLs without qualifiers (e.g., `pkg:maven/org.apache/commons-lang3@3.12` instead of `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar`).

### Evidence from PR Diff

**Service layer change (`modules/fundamental/src/purl/service/mod.rs`):**

The service layer now strips qualifiers from the PURL before serializing:

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

The `without_qualifiers()` method is called on each PURL entity before converting to the summary response, ensuring all qualifiers are stripped.

**Endpoint layer change (`modules/fundamental/src/purl/endpoints/recommend.rs`):**

The `JoinType` import for qualifier joins was removed, confirming qualifier data is no longer fetched.

**Test confirmation (`tests/api/purl_recommend.rs`):**

The `test_recommend_purls_basic` test now asserts:

```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This directly verifies that the response contains a versioned PURL without qualifiers.

### Conclusion

The code changes in the service layer use `without_qualifiers()` to strip qualifier data, and the test assertion directly verifies the expected output format. The criterion is satisfied.
