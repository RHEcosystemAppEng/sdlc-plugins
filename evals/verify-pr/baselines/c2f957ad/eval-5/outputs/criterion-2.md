# Criterion 2: Response PURLs do not contain `?` query parameters (no qualifiers present)

**Verdict: PASS**

## Code inspected
- In `modules/fundamental/src/purl/service/mod.rs`, every item in `items` is built from `p.without_qualifiers().to_string()`.
- No code path still serializes the raw qualified PURL. The old `p.to_string()` was replaced, not kept as a second branch.
- The query no longer joins `PurlQualifier`, so no qualifier data reaches the response.

## Tests
- `test_recommend_purls_basic`: `assert!(!body.items[0].purl.contains('?'))` and `assert!(!body.items[1].purl.contains('?'))`. Both returned items are checked.
- `test_simplified_purl_no_version`: `assert!(!body.items[0].purl.contains('?'))`.
- `test_simplified_purl_ordering_preserved`: checks for no `?` on both items in the page.
- `test_simplified_purl_mixed_types`: `assert!(!...contains("vcs_url"))`, plus an exact match on `pkg:npm/%40angular/core@16.0.0`, which has no `?`.

## Assessment
The criterion is enforced by construction in the service layer and checked directly by several tests across both test files.
