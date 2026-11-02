# Criterion 1: Versioned PURLs without qualifiers

**Criterion:** `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

**Verdict: PASS**

## Evidence

The implementation strips qualifiers from the PURL response at the service layer:

1. **Service change (`modules/fundamental/src/purl/service/mod.rs`):** The recommend method now calls `p.without_qualifiers()` on each result before constructing the `PurlSummary`:
   ```rust
   .map(|p| {
       let simplified = p.without_qualifiers();
       PurlSummary {
           purl: simplified.to_string(),
       }
   })
   ```
   This ensures every returned PURL is a versioned form without qualifiers.

2. **Qualifier join removed (`modules/fundamental/src/purl/service/mod.rs`):** The `JoinType::LeftJoin` on `purl::Relation::PurlQualifier` was removed from the query, confirming qualifiers are no longer fetched from the database.

3. **Import cleanup (`modules/fundamental/src/purl/endpoints/recommend.rs`):** The `use sea_orm::JoinType` import was removed, consistent with the qualifier join removal.

4. **Test verification (`tests/api/purl_recommend.rs`):** `test_recommend_purls_basic` asserts the response contains `pkg:maven/org.apache/commons-lang3@3.12` (versioned, no qualifiers) and confirms no `?` is present in the PURL string.
