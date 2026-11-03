# Criterion 2 — PASS

**Criterion:** Response PURLs do not contain `?` query parameters (no qualifiers present).

## What was checked
- Every item in the response is built from `p.without_qualifiers().to_string()` (service/mod.rs). No other code path builds `PurlSummary.purl`, so no qualifier string (`?key=value`) can reach the response.
- The qualifier join is removed from the query, so qualifier rows are no longer read at all.

## Test evidence
- `test_recommend_purls_basic`: `assert!(!body.items[0].purl.contains('?'))` and `assert!(!body.items[1].purl.contains('?'))`.
- `test_simplified_purl_no_version`: `assert!(!body.items[0].purl.contains('?'))` for an unversioned PURL.
- `test_simplified_purl_mixed_types`: an npm PURL with a `vcs_url` qualifier comes back as `pkg:npm/%40angular/core@16.0.0`, with an explicit check that it does not contain `vcs_url`.
- `test_simplified_purl_ordering_preserved`: both returned items are checked for the absence of `?`.
- `test_recommend_purls_dedup`: exact equality with `pkg:maven/org.apache/commons-lang3@3.12`.
- CI passes.

**Verdict: PASS**
