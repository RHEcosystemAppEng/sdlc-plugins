# Criterion 1: `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

**Verdict: PASS**

## Reasoning
- In `modules/fundamental/src/purl/service/mod.rs`, each item used to be built with `PurlSummary { purl: p.to_string() }`. It is now built with `let simplified = p.without_qualifiers(); PurlSummary { purl: simplified.to_string() }`. This is the `without_qualifiers()` builder method the task's Implementation Notes ask for (`common/src/purl.rs`).
- `without_qualifiers()` keeps type, namespace, name and version, so the output is still versioned. For example, `pkg:maven/org.apache/commons-lang3@3.12?repository_url=...&type=jar` becomes `pkg:maven/org.apache/commons-lang3@3.12`.
- The LEFT JOIN to `PurlQualifier` has been removed from the query, along with the unused `use sea_orm::JoinType;` import in `endpoints/recommend.rs`.

## Test evidence
- The updated `test_recommend_purls_basic` (`tests/api/purl_recommend.rs`) calls exactly this endpoint and asserts `body.items[0].purl == "pkg:maven/org.apache/commons-lang3@3.12"`.
- `test_simplified_purl_mixed_types` (`tests/api/purl_simplify.rs`) checks the same behaviour for npm (`pkg:npm/%40angular/core@16.0.0`).
- All CI checks pass.

## Caveat
`common/src/purl.rs` is not in the diff. The behaviour of `without_qualifiers()` is inferred from the task notes and the passing tests.
