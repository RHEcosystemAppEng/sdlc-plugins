## Criterion 2: Response PURLs do not contain `?` query parameters (no qualifiers present)

**Result: PASS**

### Evidence

The PR adds explicit assertions in multiple test functions that verify PURLs do not contain the `?` character (which would indicate qualifiers are present).

In `tests/api/purl_recommend.rs`, `test_recommend_purls_basic`:

```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

In `tests/api/purl_simplify.rs`, `test_simplified_purl_no_version`:

```rust
assert!(!body.items[0].purl.contains('?'));
```

In `tests/api/purl_simplify.rs`, `test_simplified_purl_ordering_preserved`:

```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

The implementation in `modules/fundamental/src/purl/service/mod.rs` achieves this by calling `p.without_qualifiers()` which removes the qualifier portion of the PURL before serialization.

Additionally, the `JoinType::LeftJoin` on `purl::Relation::PurlQualifier` has been removed from the endpoint handler in `recommend.rs`, and the sea_orm `JoinType` import has been removed entirely, confirming qualifiers are no longer part of the query.

### Conclusion

Response PURLs are confirmed to not contain `?` query parameters. The implementation strips qualifiers at the service layer and multiple tests assert the absence of the `?` character.
