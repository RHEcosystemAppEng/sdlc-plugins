# Criterion 2: Response PURLs do not contain `?` query parameters (no qualifiers present)

## Verdict: PASS

## Reasoning

### Code Changes

This criterion is a direct consequence of the same code change that satisfies Criterion 1. In `modules/fundamental/src/purl/service/mod.rs`, `p.without_qualifiers()` strips all qualifier key-value pairs from the PURL. Since qualifiers appear after the `?` character in PURL syntax (e.g., `pkg:type/namespace/name@version?key=value`), removing qualifiers removes the `?` and everything after it.

The `without_qualifiers()` method is provided by the `PackageUrl` builder in `common/src/purl.rs` (referenced in the task's Implementation Notes), which constructs PURLs without the qualifier component.

### Test Verification

Multiple tests explicitly assert the absence of `?` in response PURLs using negative assertions:

In `tests/api/purl_recommend.rs` (`test_recommend_purls_basic`):
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

In `tests/api/purl_simplify.rs` (`test_simplified_purl_no_version`):
```rust
assert!(!body.items[0].purl.contains('?'));
```

In `tests/api/purl_simplify.rs` (`test_simplified_purl_ordering_preserved`):
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

In `tests/api/purl_simplify.rs` (`test_simplified_purl_mixed_types`):
```rust
assert!(!body.items[0].purl.contains("vcs_url"));
```

### Conclusion

The `without_qualifiers()` call guarantees no qualifier parameters appear in the response, and five separate negative assertions across two test files confirm that `?` query parameters are absent from response PURLs. The criterion is satisfied.
