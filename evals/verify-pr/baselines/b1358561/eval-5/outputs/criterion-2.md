# Criterion 2 — PASS

**Criterion:** Response PURLs do not contain `?` query parameters (no qualifiers present).

## Reasoning

- `PurlService::recommend` builds every `PurlSummary` from `p.without_qualifiers().to_string()`. No other code path in the function builds an item, so no qualifier string (`?key=value`) can reach the response.
- Tests assert this directly:
  - `tests/api/purl_recommend.rs::test_recommend_purls_basic` asserts `!body.items[0].purl.contains('?')` and `!body.items[1].purl.contains('?')`.
  - `tests/api/purl_simplify.rs::test_simplified_purl_no_version` asserts `!contains('?')`.
  - `tests/api/purl_simplify.rs::test_simplified_purl_mixed_types` asserts `!contains("vcs_url")` and an exact match on `pkg:npm/%40angular/core@16.0.0`.
  - `tests/api/purl_simplify.rs::test_simplified_purl_ordering_preserved` asserts `!contains('?')` on both items it returns.
