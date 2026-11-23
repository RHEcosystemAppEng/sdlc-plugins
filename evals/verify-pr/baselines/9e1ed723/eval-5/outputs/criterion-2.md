# Criterion 2

**Criterion:** Response PURLs do not contain `?` query parameters (no qualifiers present)

**Verdict:** PASS

## Evidence

- Every item in the response goes through `p.without_qualifiers()` before `to_string()` in
  `PurlService::recommend`. No code path serializes the original qualified PURL.
- In PURL syntax, `?` only appears to start the qualifiers. Removing qualifiers therefore removes the `?`.
- Tests that assert there is no `?`:
  - `test_recommend_purls_basic`: `assert!(!body.items[0].purl.contains('?'))` and the same check on `items[1]`.
  - `test_simplified_purl_no_version`: `assert!(!body.items[0].purl.contains('?'))`.
  - `test_simplified_purl_mixed_types`: `assert!(!body.items[0].purl.contains("vcs_url"))` together with an exact-match assertion
    `"pkg:npm/%40angular/core@16.0.0"`.
  - `test_simplified_purl_ordering_preserved`: checks for no `?` on both returned items.

## Conclusion

The implementation and several tests confirm this criterion.
