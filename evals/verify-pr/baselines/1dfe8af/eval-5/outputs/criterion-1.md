# Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

## Verdict: PASS

## Reasoning

The PR implements this criterion through a code change in the service layer and validates it with updated tests.

1. **Qualifier join removed:** In `modules/fundamental/src/purl/endpoints/recommend.rs`, the `use sea_orm::JoinType;` import is removed, and in `modules/fundamental/src/purl/service/mod.rs`, the line `.join(JoinType::LeftJoin, purl::Relation::PurlQualifier.def())` is deleted from the recommend query. This means the query no longer joins against qualifier data at all.

2. **Qualifier stripping in serialization:** The mapping logic in `modules/fundamental/src/purl/service/mod.rs` is changed from directly converting the PURL to string:
   ```rust
   .map(|p| PurlSummary {
       purl: p.to_string(),
   })
   ```
   to first calling `without_qualifiers()`:
   ```rust
   .map(|p| {
       let simplified = p.without_qualifiers();
       PurlSummary {
           purl: simplified.to_string(),
       }
   })
   ```
   The `without_qualifiers()` method is documented in the task as being available on the `PackageUrl` builder in `common/src/purl.rs`.

3. **Test validation:** The updated `test_recommend_purls_basic` asserts:
   ```rust
   assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
   ```
   This confirms the endpoint returns a versioned PURL (includes `@3.12`) without qualifiers (no `?repository_url=...` suffix).

The code change and test assertion together confirm this criterion is satisfied.
