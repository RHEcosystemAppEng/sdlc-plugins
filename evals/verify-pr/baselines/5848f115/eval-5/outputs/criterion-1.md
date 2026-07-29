# Criterion 1: GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3 returns versioned PURLs without qualifiers

## Verdict: PASS

## Reasoning

### Code Changes

In `modules/fundamental/src/purl/service/mod.rs`, the recommendation service was modified to strip qualifiers from returned PURLs. The key change is:

```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

Previously, the code used `p.to_string()` which included the full PURL with qualifiers. Now it calls `p.without_qualifiers()` before serialization, producing versioned PURLs like `pkg:maven/org.apache/commons-lang3@3.12` instead of `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar`.

The qualifier join was also removed from the query:
```rust
// Before:
.join(JoinType::LeftJoin, purl::Relation::PurlQualifier.def());
// After: join removed entirely
```

This ensures qualifier data is not fetched from the database at all.

### Test Verification

`test_recommend_purls_basic` in `tests/api/purl_recommend.rs` directly validates this criterion:

```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

The test seeds PURLs with qualifiers (`?repository_url=...&type=jar`) but asserts the response contains only the versioned form without qualifiers. This confirms the endpoint returns versioned PURLs without qualifiers as required.

Additionally, `test_simplified_purl_mixed_types` in `tests/api/purl_simplify.rs` confirms this works for non-Maven PURL types:

```rust
assert_eq!(body.items[0].purl, "pkg:npm/%40angular/core@16.0.0");
```

### Conclusion

The service layer code change (`without_qualifiers()`) directly implements this criterion, and multiple tests validate the expected response format. The criterion is satisfied.
