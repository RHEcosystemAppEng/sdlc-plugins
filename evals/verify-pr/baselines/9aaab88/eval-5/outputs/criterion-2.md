# Criterion 2: Response PURLs do not contain `?` query parameters (no qualifiers present)

## Verdict: PASS

## Reasoning

The `without_qualifiers()` method is called on each PURL before serialization in the service layer (`modules/fundamental/src/purl/service/mod.rs`). This strips any qualifier key-value pairs that would appear after the `?` separator in a PURL string.

Multiple tests explicitly verify this behavior:

1. **`test_recommend_purls_basic`** in `tests/api/purl_recommend.rs`:
   ```rust
   assert!(!body.items[0].purl.contains('?'));
   assert!(!body.items[1].purl.contains('?'));
   ```

2. **`test_simplified_purl_no_version`** in `tests/api/purl_simplify.rs`:
   ```rust
   assert!(!body.items[0].purl.contains('?'));
   ```

3. **`test_simplified_purl_mixed_types`** in `tests/api/purl_simplify.rs`:
   ```rust
   assert!(!body.items[0].purl.contains("vcs_url"));
   ```

4. **`test_simplified_purl_ordering_preserved`** in `tests/api/purl_simplify.rs`:
   ```rust
   assert!(!body.items[0].purl.contains('?'));
   assert!(!body.items[1].purl.contains('?'));
   ```

The combination of the service layer code change (calling `without_qualifiers()`) and the explicit `!contains('?')` assertions across multiple tests confirms that response PURLs do not contain query parameter qualifiers. The criterion is satisfied.
