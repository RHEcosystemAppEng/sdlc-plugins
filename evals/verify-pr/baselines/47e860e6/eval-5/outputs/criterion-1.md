# Criterion 1: `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

**Verdict: PASS**

## Evidence
- `modules/fundamental/src/purl/service/mod.rs`: the mapping changed from `PurlSummary { purl: p.to_string() }` to:
  ```rust
  let simplified = p.without_qualifiers();
  PurlSummary { purl: simplified.to_string() }
  ```
  This uses the `without_qualifiers()` method named in the Implementation Notes. It strips only the qualifiers and keeps the version (`@3.12`).
- The qualifier `LeftJoin` (`purl::Relation::PurlQualifier`) was removed from the recommendation query, as the task required. The unused `use sea_orm::JoinType;` import was removed from `endpoints/recommend.rs`.
- The namespace and name filters are unchanged, so the same package's rows still match.

## Test coverage
- `test_recommend_purls_basic` now asserts `body.items[0].purl == "pkg:maven/org.apache/commons-lang3@3.12"`, a versioned PURL without qualifiers.
- `test_simplified_purl_mixed_types` checks the same thing for npm (`pkg:npm/%40angular/core@16.0.0`).

## Caveat (does not change the verdict)
`test_recommend_purls_basic` assumes `items[0]` is the 3.12 row, but the query has no `ORDER BY` (see criterion 4). The test therefore depends on the database returning rows in a particular order and could be flaky. The behaviour this criterion asks for is implemented.
