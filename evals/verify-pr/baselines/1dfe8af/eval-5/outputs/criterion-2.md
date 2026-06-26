# Criterion 2: Response PURLs do not contain `?` query parameters (no qualifiers present)

## Verdict: PASS

## Reasoning

The PR guarantees qualifier absence through the code change and confirms it with explicit assertions in multiple tests.

1. **Code mechanism:** In `modules/fundamental/src/purl/service/mod.rs`, the `without_qualifiers()` method is called on every PURL before serialization into `PurlSummary`. This method strips all qualifier key-value pairs -- the components that appear after the `?` character in a PURL string.

2. **Direct assertions in modified test file:** The updated `test_recommend_purls_basic` in `tests/api/purl_recommend.rs` explicitly checks for the absence of `?`:
   ```rust
   assert!(!body.items[0].purl.contains('?'));
   assert!(!body.items[1].purl.contains('?'));
   ```

3. **Assertions in new test file:** The new `tests/api/purl_simplify.rs` includes qualifier-absence assertions across all three test functions:
   - `test_simplified_purl_no_version`: `assert!(!body.items[0].purl.contains('?'));`
   - `test_simplified_purl_mixed_types`: `assert!(!body.items[0].purl.contains("vcs_url"));`
   - `test_simplified_purl_ordering_preserved`: `assert!(!body.items[0].purl.contains('?'));` and `assert!(!body.items[1].purl.contains('?'));`

The service-layer stripping combined with multiple negative assertions across both test files provides strong evidence that response PURLs will not contain `?` query parameters.
