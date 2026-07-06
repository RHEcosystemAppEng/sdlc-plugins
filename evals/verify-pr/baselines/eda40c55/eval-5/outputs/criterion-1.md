# Criterion 1: `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

## Verdict: PASS

## Analysis

The PR modifies the service layer in `modules/fundamental/src/purl/service/mod.rs` to strip qualifiers from PURLs before returning them. The key change is:

```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

This calls `without_qualifiers()` on each PURL entity before converting to string, which strips all qualifier parameters (everything after `?` in the PURL format).

## Test Evidence

The test `test_recommend_purls_basic` in `tests/api/purl_recommend.rs` directly verifies this behavior:

- Seeds PURLs with qualifiers: `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar`
- Asserts the response contains the versioned form without qualifiers: `assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12")`

The test passes (all CI checks pass), confirming the endpoint returns versioned PURLs without qualifiers.

## Conclusion

The criterion is satisfied. The production code applies `without_qualifiers()` and tests verify the output format matches the versioned-without-qualifiers expectation.
