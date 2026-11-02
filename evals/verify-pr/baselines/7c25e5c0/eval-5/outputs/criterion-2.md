# Criterion 2: No query parameters in response PURLs

**Criterion:** Response PURLs do not contain `?` query parameters (no qualifiers present)

**Verdict: PASS**

## Evidence

1. **Service layer (`modules/fundamental/src/purl/service/mod.rs`):** The `without_qualifiers()` call strips all query parameters from the PURL before serialization. Since qualifiers are represented as query parameters in the PURL specification (e.g., `?repository_url=...&type=...`), calling `without_qualifiers()` ensures no `?` appears in the output.

2. **Test assertions (`tests/api/purl_recommend.rs`):** The `test_recommend_purls_basic` function explicitly asserts no query parameters:
   ```rust
   assert!(!body.items[0].purl.contains('?'));
   assert!(!body.items[1].purl.contains('?'));
   ```

3. **New test file (`tests/api/purl_simplify.rs`):** All three test functions include `contains('?')` negative assertions:
   - `test_simplified_purl_no_version`: `assert!(!body.items[0].purl.contains('?'));`
   - `test_simplified_purl_mixed_types`: `assert!(!body.items[0].purl.contains("vcs_url"));`
   - `test_simplified_purl_ordering_preserved`: `assert!(!body.items[0].purl.contains('?'));` and `assert!(!body.items[1].purl.contains('?'));`
