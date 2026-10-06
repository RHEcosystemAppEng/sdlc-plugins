# Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

## Verdict: PASS

## Reasoning

The PR satisfies this criterion through changes in both the service layer and the test suite.

### Service Layer Changes

In `modules/fundamental/src/purl/service/mod.rs`, the PURL serialization logic was changed from:

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

The `without_qualifiers()` method strips all qualifier parameters from the PURL before converting it to a string. This means the response will contain versioned PURLs like `pkg:maven/org.apache/commons-lang3@3.12` instead of `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar`.

Additionally, the `JoinType::LeftJoin` to `purl::Relation::PurlQualifier` was removed from the query, confirming that qualifier data is no longer fetched from the database.

### Test Evidence

The `test_recommend_purls_basic` test seeds PURLs with qualifiers but asserts the response contains only versioned PURLs without qualifiers:

```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

The new `test_simplified_purl_mixed_types` test in `purl_simplify.rs` further confirms this behavior across different PURL types (npm, pypi).

### Conclusion

The endpoint now returns versioned PURLs without qualifiers, as confirmed by both the implementation change (`without_qualifiers()`) and the updated test assertions.
