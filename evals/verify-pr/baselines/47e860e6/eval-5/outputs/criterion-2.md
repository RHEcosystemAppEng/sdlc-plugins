# Criterion 2: Response PURLs do not contain `?` query parameters (no qualifiers present)

**Verdict: PASS**

## Evidence
- Every item is passed through `without_qualifiers()` before `to_string()` in `PurlService::recommend`. No code path in the diff returns an unstripped `p.to_string()`, so no `?qualifier=...` part can be produced.

## Test coverage
- `test_recommend_purls_basic`: asserts `!contains('?')` on both items.
- `test_simplified_purl_no_version`: asserts `!contains('?')`.
- `test_simplified_purl_ordering_preserved`: asserts `!contains('?')` on both items.
- `test_simplified_purl_mixed_types`: asserts the exact PURL string without qualifiers and `!contains("vcs_url")`.

## Minor note
PURL subpaths (`#...`) are not tested. That is outside this criterion, which only covers `?` qualifiers.
