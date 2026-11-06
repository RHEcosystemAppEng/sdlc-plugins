# Criterion 2

**Criterion:** Response PURLs do not contain `?` query parameters (no qualifiers present)

**Verdict:** PASS

## What was checked

- In `modules/fundamental/src/purl/service/mod.rs`, each item's `purl` field is built from `p.without_qualifiers().to_string()`. A PURL with no qualifiers serializes without the `?key=value` part. No other code path in the diff builds `PurlSummary.purl`.
- The qualifier join was removed, so qualifier data is no longer fetched for this query at all.

## Test evidence

- `test_recommend_purls_basic`: `assert!(!body.items[0].purl.contains('?'));` and `assert!(!body.items[1].purl.contains('?'));`
- `test_simplified_purl_no_version`: `assert!(!body.items[0].purl.contains('?'));`
- `test_simplified_purl_mixed_types`: `assert!(!body.items[0].purl.contains("vcs_url"));` plus an exact-match assertion with no `?`
- `test_simplified_purl_ordering_preserved`: both returned items are asserted to contain no `?`
- `test_recommend_purls_dedup`: exact match `pkg:maven/org.apache/commons-lang3@3.12`

Every returned item is covered, both by the code path and by the tests.
