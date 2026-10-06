# Criterion 2: Response PURLs do not contain `?` query parameters (no qualifiers present)

## Verdict: PASS

## Evidence

### Production code

The service layer in `modules/fundamental/src/purl/service/mod.rs` calls `p.without_qualifiers()` on every PURL before constructing the `PurlSummary`. Since `without_qualifiers()` strips the query string portion of the PURL, no `?` character or qualifier key-value pairs appear in the serialized output.

### Test assertions

Multiple tests explicitly assert the absence of `?` in response PURLs:

**In `tests/api/purl_recommend.rs` (`test_recommend_purls_basic`):**
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

**In `tests/api/purl_simplify.rs` (`test_simplified_purl_no_version`):**
```rust
assert!(!body.items[0].purl.contains('?'));
```

**In `tests/api/purl_simplify.rs` (`test_simplified_purl_mixed_types`):**
```rust
assert!(!body.items[0].purl.contains("vcs_url"));
```

**In `tests/api/purl_simplify.rs` (`test_simplified_purl_ordering_preserved`):**
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

### Conclusion

Both negative assertions (`!contains('?')`) and positive exact-match assertions (e.g., comparing to `"pkg:maven/org.apache/commons-lang3@3.12"`) confirm that response PURLs contain no query parameters.
