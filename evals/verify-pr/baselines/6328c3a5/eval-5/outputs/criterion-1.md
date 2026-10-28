# Criterion 1: GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3 returns versioned PURLs without qualifiers

## Verdict: PASS

## Reasoning

The production code changes directly implement this criterion through two modifications:

**Service layer (`modules/fundamental/src/purl/service/mod.rs`)**:
The recommendation query was changed to strip qualifiers from the returned PURLs. The mapping function now calls `p.without_qualifiers()` before serialization:

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

**Endpoint layer (`modules/fundamental/src/purl/endpoints/recommend.rs`)**:
The `JoinType` import was removed since qualifier joins are no longer performed. The endpoint signature and return type remain unchanged.

**Test evidence**: The modified `test_recommend_purls_basic` test seeds PURLs with qualifiers (`?repository_url=...&type=jar`) but asserts the response contains only the versioned form:

```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This directly validates that the endpoint returns versioned PURLs without qualifiers. Additionally, `test_simplified_purl_no_version` in the new `purl_simplify.rs` file confirms the behavior extends to PURLs without versions, and `test_simplified_purl_mixed_types` confirms it works across different PURL types (npm, pypi).
