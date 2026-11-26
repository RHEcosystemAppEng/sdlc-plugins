# Criterion 2: Response PURLs do not contain `?` query parameters (no qualifiers present)

**Verdict: PASS**

## What was checked
- Every item in the response is built from `p.without_qualifiers().to_string()` in
  `PurlService::recommend` (`modules/fundamental/src/purl/service/mod.rs`). No other code path builds
  `PurlSummary.purl` for this endpoint.
- The query no longer joins `PurlQualifier`, so qualifier data never reaches the mapping.

## Test evidence
- `test_recommend_purls_basic`: `assert!(!body.items[0].purl.contains('?'))` and
  `assert!(!body.items[1].purl.contains('?'))`. This covers every item in the response, not only
  the first.
- `test_simplified_purl_no_version`: `assert!(!body.items[0].purl.contains('?'))`.
- `test_simplified_purl_mixed_types`: `assert!(!body.items[0].purl.contains("vcs_url"))`, plus an exact
  equality check on the qualifier-free string.
- `test_simplified_purl_ordering_preserved`: both returned items are checked for the absence of `?`.

## Conclusion
No `?` qualifier section can appear in response PURLs. The criterion is met.
