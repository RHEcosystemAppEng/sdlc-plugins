# Criterion 1: Returns versioned PURLs without qualifiers

## Verdict: PASS

## Criterion

`GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers.

## Evidence

The implementation in `modules/fundamental/src/purl/service/mod.rs` applies `without_qualifiers()` to each PURL before constructing the `PurlSummary` response:

```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

The test `test_recommend_purls_basic` in `tests/api/purl_recommend.rs` confirms this behavior by asserting:

```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This assertion checks that the returned PURL is versioned (`@3.12`) but does not include qualifiers. The seeds still include qualifiers (`?repository_url=...&type=jar`), demonstrating that qualifiers are stripped during response construction.
