## Criterion 2: Response PURLs do not contain `?` query parameters (no qualifiers present)

### Verdict: PASS

### Analysis

The `without_qualifiers()` method strips all query parameters from the PURL string. Since PURL qualifiers are encoded as query parameters (after the `?` character), calling `without_qualifiers()` ensures no `?` appears in the serialized PURL.

**Test coverage**: Multiple test functions explicitly assert the absence of `?`:

In `test_recommend_purls_basic` (modified):
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

In `test_simplified_purl_no_version` (new):
```rust
assert!(!body.items[0].purl.contains('?'));
```

In `test_simplified_purl_mixed_types` (new):
```rust
assert!(!body.items[0].purl.contains("vcs_url"));
```

In `test_simplified_purl_ordering_preserved` (new):
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

The negative assertions (`!contains('?')`) directly verify this criterion. The test data includes PURLs seeded with qualifiers (`repository_url=`, `type=`, `vcs_url=`), ensuring the stripping is tested against real qualifier content.
