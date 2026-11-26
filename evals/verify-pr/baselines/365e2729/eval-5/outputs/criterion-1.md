# Criterion 1: `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

**Verdict: PASS**

## What was checked
- `modules/fundamental/src/purl/service/mod.rs` (`PurlService::recommend`): the mapping closure changed from
  `PurlSummary { purl: p.to_string() }` to
  `let simplified = p.without_qualifiers(); PurlSummary { purl: simplified.to_string() }`.
  This is the `without_qualifiers()` builder method that the task's Implementation Notes call for
  (`common/src/purl.rs`).
- The qualifier join (`.join(JoinType::LeftJoin, purl::Relation::PurlQualifier.def())`) was removed
  from the query, and the now-unused `use sea_orm::JoinType;` was removed from
  `modules/fundamental/src/purl/endpoints/recommend.rs`.
- The endpoint handler `recommend_purls` still calls `PurlService::recommend(&params.purl, offset, limit)`,
  so every endpoint response goes through the simplified mapping.

## Test evidence
- `tests/api/purl_recommend.rs::test_recommend_purls_basic` seeds
  `pkg:maven/org.apache/commons-lang3@3.12?repository_url=...&type=jar` and `@3.11?...`, requests
  `/api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3`, and asserts
  `body.items[0].purl == "pkg:maven/org.apache/commons-lang3@3.12"`. That is the versioned PURL with
  no qualifiers, the exact URL in the criterion.
- `tests/api/purl_simplify.rs::test_simplified_purl_mixed_types` asserts the same thing for npm
  (`pkg:npm/%40angular/core@16.0.0`).

## Conclusion
The version is kept and the qualifiers are dropped. The criterion is met.
