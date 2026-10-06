# Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

## Verdict: PASS

## Evidence

### Production code changes

In `modules/fundamental/src/purl/service/mod.rs`, the service layer now strips qualifiers before serialization:

```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

Previously, the code serialized PURLs directly via `p.to_string()`, which included qualifiers. The `without_qualifiers()` method produces a versioned PURL without the `?key=value` suffix.

Additionally, the qualifier join was removed from the query:

```diff
-            .join(JoinType::LeftJoin, purl::Relation::PurlQualifier.def());
+            .filter(purl::Column::Name.eq(&base_purl.name));
```

This means qualifiers are no longer fetched from the database at all.

### Test evidence

In `tests/api/purl_recommend.rs`, the `test_recommend_purls_basic` test asserts:

```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

The assertion checks that the response PURL is `pkg:maven/org.apache/commons-lang3@3.12` (versioned, no qualifiers) and that no `?` character is present (confirming no query parameters).

In `tests/api/purl_simplify.rs`, `test_simplified_purl_no_version` and `test_simplified_purl_mixed_types` further confirm that PURLs of various types are returned without qualifiers.

### Conclusion

Both the production code and the test assertions demonstrate that the endpoint now returns versioned PURLs without qualifiers.
