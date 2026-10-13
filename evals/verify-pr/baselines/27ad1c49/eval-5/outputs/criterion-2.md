# Criterion 2: Response PURLs do not contain `?` query parameters

## Criterion Text

Response PURLs do not contain `?` query parameters (no qualifiers present)

## Verdict: PASS

## Reasoning

### Code Changes

This criterion is a more specific assertion of Criterion 1. The `without_qualifiers()` call in `modules/fundamental/src/purl/service/mod.rs` strips all qualifier key-value pairs from the PURL before serialization. Since qualifiers are appended to the PURL string after a `?` delimiter in the PURL specification, removing qualifiers means no `?` character appears in the response PURL strings.

### Test Coverage

Multiple tests explicitly verify the absence of `?` in response PURLs:

**In `tests/api/purl_recommend.rs` -- `test_recommend_purls_basic`:**
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

These negative assertions directly confirm the absence of query parameters in the response, even though the seeded PURLs include qualifiers (`?repository_url=https://repo1.maven.org&type=jar`).

**In `tests/api/purl_simplify.rs` -- `test_simplified_purl_no_version`:**
```rust
assert!(!body.items[0].purl.contains('?'));
```

Tests that even PURLs without a version have no qualifiers in the response.

**In `tests/api/purl_simplify.rs` -- `test_simplified_purl_mixed_types`:**
```rust
assert!(!body.items[0].purl.contains("vcs_url"));
```

Tests that specific qualifier keys like `vcs_url` are absent for non-Maven PURL types.

**In `tests/api/purl_simplify.rs` -- `test_simplified_purl_ordering_preserved`:**
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

Verifies qualifier absence is maintained even with pagination.

### Verification Strategy

The test approach is sound: PURLs are seeded WITH qualifiers (reflecting the database content) and the response is asserted to NOT contain qualifiers. This tests the transformation layer, not just the seeding. The `contains('?')` assertion is the correct check because `?` is the PURL specification delimiter for qualifiers -- its absence confirms no qualifiers are present.

### CI Confirmation

All CI checks pass, confirming these assertions hold.

## Conclusion

The code strips qualifiers via `without_qualifiers()`, and multiple tests explicitly verify the absence of `?` query parameters in the response. This criterion is satisfied.
