# Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

## Verdict: PASS

## Analysis

The acceptance criterion requires that `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers.

### Evidence from the PR diff

The service layer in `modules/fundamental/src/purl/service/mod.rs` now calls `p.without_qualifiers()` on each PURL result before constructing the `PurlSummary`:

```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

This replaces the previous implementation which used `p.to_string()` directly (which included qualifier parameters).

The `without_qualifiers()` method is documented in the task as being supported by the `PackageUrl` builder in `common/src/purl.rs`.

### Test coverage

The updated `test_recommend_purls_basic` test explicitly asserts that the returned PURL equals `"pkg:maven/org.apache/commons-lang3@3.12"` (versioned, no qualifiers):

```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This directly validates the criterion.

### Conclusion

The implementation correctly strips qualifiers from PURL responses via the `without_qualifiers()` method, and the result is the versioned PURL format (e.g., `pkg:maven/org.apache/commons-lang3@3.12`). The criterion is satisfied.
