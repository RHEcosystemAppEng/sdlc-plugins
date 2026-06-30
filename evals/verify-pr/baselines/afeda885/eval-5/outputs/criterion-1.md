# Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

## Criterion Text
`GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

## Verdict: PASS

## Analysis

The diff shows changes across two implementation files that together accomplish this criterion:

### Endpoint layer (modules/fundamental/src/purl/endpoints/recommend.rs)
- The `sea_orm::JoinType` import was removed, indicating the qualifier join is no longer needed at the endpoint level.
- The handler function signature and return type remain unchanged (`Result<Json<PaginatedResults<PurlSummary>>, AppError>`), confirming the endpoint still serves the same route.

### Service layer (modules/fundamental/src/purl/service/mod.rs)
- The qualifier join (`JoinType::LeftJoin, purl::Relation::PurlQualifier.def()`) was removed from the recommendation query. This means qualifiers are no longer fetched from the database for this operation.
- The mapping logic was changed: instead of `p.to_string()` (which produced the fully qualified PURL), the code now calls `p.without_qualifiers()` followed by `.to_string()`, which produces a versioned PURL without qualifiers.
- The `PurlSummary` construction now uses the simplified (qualifier-free) PURL string.

### Test evidence
- In `test_recommend_purls_basic`, the assertion changed from:
  ```rust
  assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar");
  ```
  to:
  ```rust
  assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
  ```
  This confirms the endpoint now returns versioned PURLs without qualifiers.

- The new `test_simplified_purl_no_version` test in `purl_simplify.rs` further confirms PURLs are returned without qualifiers even when seeded with qualifiers.

The code changes directly implement the requirement: the query no longer joins qualifier data, and the serialization explicitly strips qualifiers via `without_qualifiers()`.
