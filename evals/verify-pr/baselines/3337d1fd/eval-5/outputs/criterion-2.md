# Criterion 2: Response PURLs do not contain `?` query parameters

## Verdict: PASS

## Analysis

This criterion requires that PURLs in the response do not contain `?` query parameters (i.e., no qualifiers are present in the serialized PURL strings).

### Evidence from PR Diff

**Service layer (`modules/fundamental/src/purl/service/mod.rs`):**

The `without_qualifiers()` method is applied to every PURL before serialization:

```rust
let simplified = p.without_qualifiers();
PurlSummary {
    purl: simplified.to_string(),
}
```

This ensures no qualifier query parameters (`?key=value`) appear in the output.

**Qualifier join removed:**

The qualifier join was removed from the query:

```diff
-            .join(JoinType::LeftJoin, purl::Relation::PurlQualifier.def());
+            .filter(purl::Column::Name.eq(&base_purl.name));
```

This means qualifier data is not even fetched from the database, providing a second layer of assurance.

**Test assertions (`tests/api/purl_recommend.rs`):**

The updated `test_recommend_purls_basic` test explicitly checks for the absence of `?`:

```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

**Additional test coverage (`tests/api/purl_simplify.rs`):**

Multiple new tests also verify no qualifiers:

- `test_simplified_purl_no_version`: `assert!(!body.items[0].purl.contains('?'));`
- `test_simplified_purl_mixed_types`: `assert!(!body.items[0].purl.contains("vcs_url"));`
- `test_simplified_purl_ordering_preserved`: `assert!(!body.items[0].purl.contains('?'));` and `assert!(!body.items[1].purl.contains('?'));`

### Conclusion

The service layer strips qualifiers using `without_qualifiers()`, the qualifier join is removed from the database query, and multiple tests explicitly assert the absence of `?` in response PURLs. The criterion is satisfied.
