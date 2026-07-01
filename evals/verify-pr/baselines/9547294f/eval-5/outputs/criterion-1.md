# Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

## Criterion Text
`GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

## Verdict: PASS

## Reasoning

The PR diff shows changes in two production files that implement this behavior:

**Service layer (`modules/fundamental/src/purl/service/mod.rs`):**
- The qualifier join is removed: the line `.join(JoinType::LeftJoin, purl::Relation::PurlQualifier.def())` is deleted.
- The mapping now calls `p.without_qualifiers()` to strip qualifiers before serialization:
  ```rust
  .map(|p| {
      let simplified = p.without_qualifiers();
      PurlSummary {
          purl: simplified.to_string(),
      }
  })
  ```

**Endpoint layer (`modules/fundamental/src/purl/endpoints/recommend.rs`):**
- The `use sea_orm::JoinType;` import is removed since the join is no longer needed.
- The endpoint handler signature and return type remain unchanged.

**Test confirmation:**
- `test_recommend_purls_basic` in the PR version asserts:
  ```rust
  assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
  ```
  This confirms the response contains a versioned PURL (`@3.12`) without qualifiers (no `?` suffix).

The code changes directly implement qualifier removal from the PURL recommendation response. The endpoint returns versioned PURLs without qualifiers as required.
