# Criterion 2: Response PURLs do not contain `?` query parameters (no qualifiers present)

## Verdict: PASS

## Analysis

This criterion requires a negative assertion: response PURLs must not contain the `?` character, which would indicate qualifier parameters are still present.

### Evidence from the PR diff

**Service layer (`modules/fundamental/src/purl/service/mod.rs`):**

The `without_qualifiers()` method is applied to every PURL before serialization:

```rust
let simplified = p.without_qualifiers();
PurlSummary {
    purl: simplified.to_string(),
}
```

This systematically removes all qualifier parameters from every PURL in the response, ensuring no `?` character appears in any serialized PURL string.

**Test assertions in modified file (`tests/api/purl_recommend.rs`):**

The `test_recommend_purls_basic` test includes explicit negative assertions:

```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

These assertions directly test the criterion's requirement. If any qualifier parameters leaked through, these assertions would fail.

**Test assertions in new file (`tests/api/purl_simplify.rs`):**

Multiple tests in the new file also assert the absence of `?`:

- `test_simplified_purl_no_version`: `assert!(!body.items[0].purl.contains('?'));`
- `test_simplified_purl_mixed_types`: `assert!(!body.items[0].purl.contains("vcs_url"));`
- `test_simplified_purl_ordering_preserved`: `assert!(!body.items[0].purl.contains('?'));` and `assert!(!body.items[1].purl.contains('?'));`

**Query layer change (`modules/fundamental/src/purl/service/mod.rs`):**

The qualifier join was also removed from the query:

```rust
// Removed: .join(JoinType::LeftJoin, purl::Relation::PurlQualifier.def());
```

This means qualifier data is not even fetched from the database, providing a defense-in-depth approach -- even if `without_qualifiers()` had a bug, there would be no qualifier data to include.

### Conclusion

The criterion is satisfied through two mechanisms: (1) the `without_qualifiers()` method strips qualifiers from each PURL, and (2) the qualifier join is removed from the query so qualifier data is never fetched. Multiple test assertions explicitly verify the absence of `?` in response PURLs.
