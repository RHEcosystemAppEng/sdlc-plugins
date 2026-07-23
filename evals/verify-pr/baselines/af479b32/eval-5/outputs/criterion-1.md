# Criterion 1: GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3 returns versioned PURLs without qualifiers

## Verdict: PASS

## Reasoning

### Code Change Analysis

The PR modifies `modules/fundamental/src/purl/service/mod.rs` to strip qualifiers from the PURL recommendation response. The key change is in the `recommend` method of `PurlService`:

```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

Previously, the code mapped directly with `p.to_string()`, which included the full PURL with qualifiers. Now it calls `without_qualifiers()` before serializing, producing a versioned PURL without the `?repository_url=...&type=...` suffix.

### Endpoint Layer

The endpoint handler in `modules/fundamental/src/purl/endpoints/recommend.rs` still calls `PurlService::recommend()` and returns `Json<PaginatedResults<PurlSummary>>`. The qualifier stripping happens at the service layer, so the endpoint correctly returns versioned PURLs without qualifiers.

### Test Verification

The updated `test_recommend_purls_basic` test explicitly verifies this behavior:
- Seeds PURLs with qualifiers: `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar`
- Asserts the response contains: `pkg:maven/org.apache/commons-lang3@3.12` (no qualifiers)

The new `tests/api/purl_simplify.rs` file further confirms this across multiple PURL types (maven, npm, pypi), each seeded with qualifiers and verified to return without qualifiers.

### Conclusion

The service layer now calls `without_qualifiers()` on each PURL before constructing the summary, and the endpoint returns these simplified PURLs. Both implementation and tests confirm the criterion is satisfied.
