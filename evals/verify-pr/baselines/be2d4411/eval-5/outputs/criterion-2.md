# Criterion 2: No Query Parameters in Response PURLs

**Criterion**: Response PURLs do not contain `?` query parameters (no qualifiers present)

**Verdict**: PASS

## Analysis

The `without_qualifiers()` method strips all qualifier key-value pairs from the PURL string representation. Since qualifiers in PURL syntax appear after the `?` character, the absence of `?` in the output string is a reliable indicator that qualifiers have been removed.

The implementation ensures this by calling `p.without_qualifiers()` on every result item before constructing the `PurlSummary`, so no PURL in the response can retain qualifiers regardless of what qualifiers existed in the database.

## Test Evidence

Multiple tests explicitly assert the absence of `?` in response PURLs:

1. **`test_recommend_purls_basic`** (`tests/api/purl_recommend.rs`):
   - `assert!(!body.items[0].purl.contains('?'));`
   - `assert!(!body.items[1].purl.contains('?'));`

2. **`test_simplified_purl_no_version`** (`tests/api/purl_simplify.rs`):
   - `assert!(!body.items[0].purl.contains('?'));`

3. **`test_simplified_purl_mixed_types`** (`tests/api/purl_simplify.rs`):
   - `assert!(!body.items[0].purl.contains("vcs_url"));` (checks specific qualifier key absence)

4. **`test_simplified_purl_ordering_preserved`** (`tests/api/purl_simplify.rs`):
   - `assert!(!body.items[0].purl.contains('?'));`
   - `assert!(!body.items[1].purl.contains('?'));`

The breadth of coverage across different PURL types (Maven, npm, PyPI) and scenarios (no version, mixed types, pagination) provides strong confidence.
