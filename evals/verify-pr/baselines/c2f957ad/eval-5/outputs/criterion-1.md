# Criterion 1: `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

**Verdict: PASS**

## Code inspected
- `modules/fundamental/src/purl/service/mod.rs` (`PurlService::recommend`): the mapping changed from `PurlSummary { purl: p.to_string() }` to `let simplified = p.without_qualifiers(); PurlSummary { purl: simplified.to_string() }`.
  - This uses the `without_qualifiers()` builder method that the Implementation Notes call for.
  - Only the qualifier part of the PURL is dropped. Type, namespace, name and version stay.
- The qualifier `LeftJoin` on `purl::Relation::PurlQualifier` was removed from the query, as the Implementation Notes require.
- `modules/fundamental/src/purl/endpoints/recommend.rs`: the handler still delegates to `PurlService::recommend`. The only changes are removing the unused `use sea_orm::JoinType;` and one whitespace-only line. Qualifiers are stripped in the service layer, which every caller of the endpoint goes through.

## Tests
- `tests/api/purl_recommend.rs::test_recommend_purls_basic` (updated):
  - Seeds `commons-lang3@3.12?repository_url=...&type=jar` and `@3.11?...`.
  - Calls exactly the endpoint and query named in the criterion.
  - Asserts `body.items[0].purl == "pkg:maven/org.apache/commons-lang3@3.12"`, so the version is kept and the qualifiers are gone.
  - This updated assertion is what the Test Requirements ask for.
- `tests/api/purl_simplify.rs::test_simplified_purl_no_version` covers the edge case with no version.
- `tests/api/purl_simplify.rs::test_simplified_purl_mixed_types` checks npm PURLs: `@16.0.0` is kept and `vcs_url` is stripped.

## Caveats
- The `items[0] == 3.12` assertion depends on the database returning rows in an implicit order, because the query has no ORDER BY. The base-branch test made the same assumption, and CI passes.
- This is static analysis only. The repository is not checked out and no Serena instance is configured.
