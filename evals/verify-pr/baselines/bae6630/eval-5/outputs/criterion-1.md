# Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

## Acceptance Criterion
`GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers.

## Analysis

### Implementation Changes

In `modules/fundamental/src/purl/service/mod.rs`, the recommend method was modified to strip qualifiers from PURLs before returning them. The key change is:

```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

Previously, the PURL was serialized directly with `p.to_string()`, which included qualifiers. Now it calls `p.without_qualifiers()` before serialization.

Additionally, in `modules/fundamental/src/purl/endpoints/recommend.rs`, the `JoinType` import for `sea_orm` was removed since the qualifier join is no longer needed. The handler signature and return type remain unchanged.

### Test Coverage

In `tests/api/purl_recommend.rs`, the `test_recommend_purls_basic` test was updated:
- Seeds PURLs with qualifiers (unchanged input data)
- Now asserts the response contains versioned PURLs WITHOUT qualifiers: `assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12")`
- Adds negative assertions: `assert!(!body.items[0].purl.contains('?'))` and `assert!(!body.items[1].purl.contains('?'))`

In the new file `tests/api/purl_simplify.rs`, the `test_simplified_purl_no_version` and `test_simplified_purl_mixed_types` tests further confirm that PURLs are returned without qualifiers across different package types (npm, pypi, maven).

### Verdict

**PASS** -- The implementation strips qualifiers using `without_qualifiers()` and tests verify that the response PURLs do not contain qualifier parameters.
