# Criterion 1

**Criterion:** `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

**Verdict:** PASS

## What was checked

- `modules/fundamental/src/purl/service/mod.rs`, `PurlService::recommend`: the mapping closure changed from
  `PurlSummary { purl: p.to_string() }` to:
  ```rust
  let simplified = p.without_qualifiers();
  PurlSummary { purl: simplified.to_string() }
  ```
  Every returned item is now serialized from a qualifier-stripped PURL. This uses the `without_qualifiers()` method that the task's Implementation Notes call for.
- The left join to `purl::Relation::PurlQualifier` was removed from the query, as the task requires ("the join was only needed for qualifier inclusion").
- `modules/fundamental/src/purl/endpoints/recommend.rs`: the handler still calls `PurlService::recommend` and returns its result. The only change is removing the now-unused `use sea_orm::JoinType;` import, plus one line that changed only in whitespace. The service layer does all the stripping, so the endpoint returns stripped PURLs.
- Version is preserved: `without_qualifiers()` drops only the qualifier component, so `@<version>` stays.

## Test evidence

- `test_recommend_purls_basic` (updated) seeds `pkg:maven/org.apache/commons-lang3@3.12?repository_url=...&type=jar` and `@3.11?...`, calls the exact endpoint in the criterion, and asserts `body.items[0].purl == "pkg:maven/org.apache/commons-lang3@3.12"`. That is a versioned PURL with no qualifiers.
- `test_simplified_purl_mixed_types` (new) shows the same for npm: `pkg:npm/%40angular/core@16.0.0`.

## Notes

- The code calls `without_qualifiers()` on the entity model `p`. The task says this method is on the `PackageUrl` builder in `common/src/purl.rs`, so `p` must be (or convert to) that type. CI passes, so it compiles.
