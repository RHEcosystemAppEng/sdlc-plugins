# Criterion 2: Response PURLs do not contain ? query parameters

## Verdict: PASS

## Analysis

The acceptance criterion requires that response PURLs do not contain `?` query parameters (i.e., no qualifiers are present in the returned PURL strings).

### Evidence from the PR diff

The implementation uses `p.without_qualifiers()` to strip all qualifier data before serializing the PURL to a string. Since qualifiers in PURL notation are appended after a `?` character (e.g., `pkg:maven/org.apache/commons-lang3@3.12?repository_url=...&type=jar`), removing qualifiers ensures no `?` character appears in the output.

### Test coverage

Multiple tests explicitly assert the absence of `?` in returned PURLs:

In `test_recommend_purls_basic`:
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

In `test_simplified_purl_no_version`:
```rust
assert!(!body.items[0].purl.contains('?'));
```

In `test_simplified_purl_mixed_types`:
```rust
assert!(!body.items[0].purl.contains("vcs_url"));
```

In `test_simplified_purl_ordering_preserved`:
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

### Conclusion

The `without_qualifiers()` call ensures no qualifier data (and thus no `?` query parameter separator) appears in the returned PURLs. Multiple tests across both test files confirm this with explicit negative assertions on the `?` character. The criterion is satisfied.
