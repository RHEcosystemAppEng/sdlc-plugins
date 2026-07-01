# Criterion 2: Response PURLs do not contain `?` query parameters

## Criterion Text
Response PURLs do not contain `?` query parameters (no qualifiers present)

## Verdict: PASS

## Reasoning

The PR implements qualifier stripping via `p.without_qualifiers()` in the service layer, which removes all qualifier key-value pairs from the PURL. The resulting `PurlSummary.purl` string is produced by calling `.to_string()` on the simplified PURL, which will not contain a `?` separator since there are no qualifiers to serialize.

**Test confirmation across multiple test files:**

In `tests/api/purl_recommend.rs`:
- `test_recommend_purls_basic` explicitly asserts the absence of `?`:
  ```rust
  assert!(!body.items[0].purl.contains('?'));
  assert!(!body.items[1].purl.contains('?'));
  ```

In `tests/api/purl_simplify.rs`:
- `test_simplified_purl_no_version` asserts `assert!(!body.items[0].purl.contains('?'));`
- `test_simplified_purl_mixed_types` asserts `assert!(!body.items[0].purl.contains("vcs_url"));` (checks a specific qualifier key is absent)
- `test_simplified_purl_ordering_preserved` asserts:
  ```rust
  assert!(!body.items[0].purl.contains('?'));
  assert!(!body.items[1].purl.contains('?'));
  ```

The production code strips qualifiers at the service layer, and multiple tests across two test files assert that `?` is not present in response PURLs. This criterion is satisfied.
