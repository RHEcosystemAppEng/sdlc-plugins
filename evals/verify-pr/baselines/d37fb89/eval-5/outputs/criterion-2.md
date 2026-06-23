# Criterion 2: Response PURLs do not contain `?` query parameters (no qualifiers present)

## Verdict: PASS

## Reasoning

The PR introduces explicit assertions in the test code to verify the absence of qualifier separators:

In `test_recommend_purls_basic` (modified test):
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

In `test_simplified_purl_no_version` (new test file `purl_simplify.rs`):
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

The service layer change in `mod.rs` calls `p.without_qualifiers()` which strips all qualifier key-value pairs before serialization. Since qualifiers are appended after a `?` in the PURL specification, removing them ensures no `?` appears in the response PURLs.

Both the implementation (service layer stripping qualifiers) and the tests (explicit `contains('?')` assertions) confirm this criterion is satisfied.
