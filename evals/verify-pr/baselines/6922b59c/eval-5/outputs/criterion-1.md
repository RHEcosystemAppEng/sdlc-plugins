## Criterion 1: `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

### Verdict: PASS

### Analysis

The service layer in `modules/fundamental/src/purl/service/mod.rs` was modified to apply `without_qualifiers()` to each PURL before building the `PurlSummary`:

```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

Previously, the code used `p.to_string()` directly, which included qualifier key-value pairs. The new code calls `without_qualifiers()` first, producing a versioned PURL like `pkg:maven/org.apache/commons-lang3@3.12` instead of `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar`.

The qualifier join (`JoinType::LeftJoin, purl::Relation::PurlQualifier.def()`) was also removed from the query, which means qualifier data is no longer fetched from the database. This is consistent -- qualifiers are neither queried nor included in the response.

**Test coverage**: The updated `test_recommend_purls_basic` function asserts:
```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```
This directly verifies the criterion. Additionally, `test_simplified_purl_no_version` and `test_simplified_purl_mixed_types` in the new test file verify this behavior for edge cases (no version, different PURL types).
