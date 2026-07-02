# Criterion 1: Versioned PURLs Without Qualifiers

**Criterion**: `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

**Verdict**: PASS

## Analysis

The implementation achieves this through two coordinated changes in the service layer (`modules/fundamental/src/purl/service/mod.rs`):

1. **Qualifier join removed**: The `JoinType::LeftJoin` on `purl::Relation::PurlQualifier` is removed from the recommendation query, so qualifier data is no longer fetched from the database.

2. **Qualifier stripping applied**: The result mapping now calls `p.without_qualifiers()` before serialization:
   ```rust
   .map(|p| {
       let simplified = p.without_qualifiers();
       PurlSummary {
           purl: simplified.to_string(),
       }
   })
   ```

The endpoint handler (`modules/fundamental/src/purl/endpoints/recommend.rs`) correspondingly removes the `use sea_orm::JoinType;` import since the join is no longer performed.

## Test Evidence

The `test_recommend_purls_basic` test in `tests/api/purl_recommend.rs` directly verifies this criterion:
- Seeds PURLs with qualifiers (`?repository_url=...&type=jar`)
- Calls the recommendation endpoint
- Asserts the response PURL is `pkg:maven/org.apache/commons-lang3@3.12` (versioned, no qualifiers)

The assertion changed from the base-branch version (which checked for the fully qualified PURL including `?repository_url=https://repo1.maven.org&type=jar`) to the simplified versioned form.
