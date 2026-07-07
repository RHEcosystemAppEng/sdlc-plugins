# Criterion 2: No query parameters in response PURLs

## Criterion Text
Response PURLs do not contain `?` query parameters (no qualifiers present)

## What was checked
Examined the service layer change that calls `without_qualifiers()` and the test assertions that explicitly check for absence of `?` in the response PURLs.

## Evidence

In `modules/fundamental/src/purl/service/mod.rs`, the `without_qualifiers()` call strips all qualifier key-value pairs (which appear after `?` in a PURL string).

The unused `JoinType` import was also removed from `modules/fundamental/src/purl/endpoints/recommend.rs`:
```rust
// Removed: use sea_orm::JoinType;
```

Multiple tests explicitly assert the absence of `?`:

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

## Verdict
PASS
