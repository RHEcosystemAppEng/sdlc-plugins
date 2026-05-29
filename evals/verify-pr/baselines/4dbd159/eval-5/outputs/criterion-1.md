## Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

**Result: PASS**

### Evidence

The PR modifies `modules/fundamental/src/purl/service/mod.rs` to strip qualifiers from the response. Specifically, the service layer now calls `p.without_qualifiers()` before serializing the PURL:

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

The test `test_recommend_purls_basic` in `tests/api/purl_recommend.rs` confirms this by asserting:

```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This is a versioned PURL without qualifiers (no `?` or query parameters), matching the criterion.

The new test file `tests/api/purl_simplify.rs` further validates this with `test_simplified_purl_mixed_types` which asserts that npm PURLs also have qualifiers stripped:

```rust
assert_eq!(body.items[0].purl, "pkg:npm/%40angular/core@16.0.0");
assert!(!body.items[0].purl.contains("vcs_url"));
```

### Conclusion

The implementation correctly strips qualifiers from PURL recommendations and returns versioned PURLs. Both modified and new tests verify this behavior.
