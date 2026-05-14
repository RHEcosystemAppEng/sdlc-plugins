# Criterion 2: Response PURLs do not contain `?` query parameters (no qualifiers present)

## Verdict: PASS

## Analysis

The PR ensures that no qualifier query parameters appear in response PURLs through two mechanisms:

1. **Service layer stripping:** In `modules/fundamental/src/purl/service/mod.rs`, the `without_qualifiers()` method is called on each PURL before serialization. This removes all qualifier key-value pairs that would appear after the `?` character.

2. **Test assertions:** The updated tests explicitly verify the absence of `?` in response PURLs:

   In `test_recommend_purls_basic`:
   ```rust
   assert!(!body.items[0].purl.contains('?'));
   assert!(!body.items[1].purl.contains('?'));
   ```

   In the new `tests/api/purl_simplify.rs` file, all three test functions assert the absence of qualifiers:
   - `test_simplified_purl_no_version`: `assert!(!body.items[0].purl.contains('?'));`
   - `test_simplified_purl_mixed_types`: `assert!(!body.items[0].purl.contains("vcs_url"));`
   - `test_simplified_purl_ordering_preserved`: `assert!(!body.items[0].purl.contains('?'));` and `assert!(!body.items[1].purl.contains('?'));`

The criterion is satisfied: response PURLs are verified to not contain `?` query parameters.
