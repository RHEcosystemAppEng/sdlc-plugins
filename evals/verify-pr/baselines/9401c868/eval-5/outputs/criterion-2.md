## Criterion 2: Response PURLs do not contain `?` query parameters

**Criterion**: Response PURLs do not contain `?` query parameters (no qualifiers present)

**Verdict**: PASS

### Analysis

The service layer change in `modules/fundamental/src/purl/service/mod.rs` calls `p.without_qualifiers()` on every PURL before serialization. This method (documented in the task as existing in `common/src/purl.rs`) strips all qualifier key-value pairs, which are the portion of the PURL after the `?` character.

Multiple tests explicitly assert the absence of `?` in response PURLs:

In `tests/api/purl_recommend.rs`, `test_recommend_purls_basic`:
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

In `tests/api/purl_simplify.rs`, `test_simplified_purl_no_version`:
```rust
assert!(!body.items[0].purl.contains('?'));
```

In `tests/api/purl_simplify.rs`, `test_simplified_purl_mixed_types`:
```rust
assert!(!body.items[0].purl.contains("vcs_url"));
```

In `tests/api/purl_simplify.rs`, `test_simplified_purl_ordering_preserved`:
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

The implementation strips qualifiers at the service layer and multiple tests verify the absence of qualifier markers in the response. The criterion is satisfied.
