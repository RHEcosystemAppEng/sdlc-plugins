# Criterion 2: Response PURLs do not contain `?` query parameters

## Verdict: PASS

## Reasoning

The criterion requires that response PURLs do not contain `?` query parameters (no qualifiers present).

The PR diff demonstrates this is satisfied through both production code changes and test assertions:

1. **Production code** (modules/fundamental/src/purl/service/mod.rs): The `without_qualifiers()` method is called on each PURL before serialization, which strips all qualifier key-value pairs. Since qualifiers are appended after a `?` in PURL syntax, removing qualifiers eliminates the `?` and everything after it from the serialized string.

2. **Test assertions** in `tests/api/purl_recommend.rs`:
   - `test_recommend_purls_basic` includes explicit assertions: `assert!(!body.items[0].purl.contains('?'))` and `assert!(!body.items[1].purl.contains('?'))`, which directly verify that no `?` character (and thus no qualifiers) appears in response PURLs.
   - `test_recommend_purls_dedup` asserts on the exact PURL string `"pkg:maven/org.apache/commons-lang3@3.12"` which contains no `?`.

3. **New test file** `tests/api/purl_simplify.rs` also contains multiple assertions verifying the absence of `?`:
   - `test_simplified_purl_no_version`: `assert!(!body.items[0].purl.contains('?'))`
   - `test_simplified_purl_mixed_types`: `assert!(!body.items[0].purl.contains("vcs_url"))`
   - `test_simplified_purl_ordering_preserved`: `assert!(!body.items[0].purl.contains('?'))` and `assert!(!body.items[1].purl.contains('?'))`

The combination of the `without_qualifiers()` call in the service layer and the comprehensive `contains('?')` assertions in tests confirms this criterion is satisfied.
