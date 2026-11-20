# Criterion 2: Response PURLs do not contain `?` query parameters (no qualifiers present)

**Verdict: PASS**

## Reasoning
- Every returned item goes through the same `.map(|p| p.without_qualifiers() ...)` step, and there is no code path that skips it. So no item in the response can keep a qualifier string.
- The qualifier join has been removed from the recommendation query, so qualifier data is not even loaded.

## Test evidence
- `test_recommend_purls_basic`: `assert!(!body.items[0].purl.contains('?'))` and `assert!(!body.items[1].purl.contains('?'))`.
- `test_simplified_purl_no_version`: `assert!(!body.items[0].purl.contains('?'))`.
- `test_simplified_purl_ordering_preserved`: `!contains('?')` on both items.
- `test_simplified_purl_mixed_types`: `!contains("vcs_url")`.
- CI passes.
