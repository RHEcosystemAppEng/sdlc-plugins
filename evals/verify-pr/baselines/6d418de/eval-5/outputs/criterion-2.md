# Criterion 2: Response PURLs do not contain `?` query parameters (no qualifiers present)

## Verdict: PASS

## Reasoning

The code change in `modules/fundamental/src/purl/service/mod.rs` applies `p.without_qualifiers()` to every PURL before serialization. The `without_qualifiers()` method strips all qualifier key-value pairs from the PURL, which means the `?` delimiter and everything after it is removed from the PURL string representation.

The tests explicitly verify this behavior with negative assertions:
- `test_recommend_purls_basic`: `assert!(!body.items[0].purl.contains('?'));` and `assert!(!body.items[1].purl.contains('?'));`
- `test_simplified_purl_no_version`: `assert!(!body.items[0].purl.contains('?'));`
- `test_simplified_purl_mixed_types`: `assert!(!body.items[0].purl.contains("vcs_url"));`
- `test_simplified_purl_ordering_preserved`: `assert!(!body.items[0].purl.contains('?'));` and `assert!(!body.items[1].purl.contains('?'));`

These assertions cover multiple scenarios (versioned, unversioned, different package types) and all confirm the absence of `?` query parameters.

## Evidence

- `modules/fundamental/src/purl/service/mod.rs`: `let simplified = p.without_qualifiers();` applied to every result item
- `tests/api/purl_recommend.rs`: `assert!(!body.items[0].purl.contains('?'));` on both items
- `tests/api/purl_simplify.rs`: Multiple `contains('?')` negative assertions across 3 test functions
