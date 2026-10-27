# Criterion 1: Versioned PURLs without qualifiers

**Criterion:** `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

**Result:** PASS

## Analysis

The diff in `modules/fundamental/src/purl/service/mod.rs` shows the critical change:

1. **Qualifier join removed:** The line `.join(JoinType::LeftJoin, purl::Relation::PurlQualifier.def())` is removed from the recommendation query, so qualifier data is no longer fetched from the database.

2. **Qualifier stripping applied:** The mapping pipeline now calls `p.without_qualifiers()` before serialization:
   ```rust
   .map(|p| {
       let simplified = p.without_qualifiers();
       PurlSummary {
           purl: simplified.to_string(),
       }
   })
   ```

3. **Test verification:** `test_recommend_purls_basic` in `tests/api/purl_recommend.rs` seeds PURLs with qualifiers (`?repository_url=...&type=jar`) but asserts the response contains only versioned PURLs:
   ```rust
   assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
   ```

The endpoint handler in `recommend.rs` maintains the same return type `Result<Json<PaginatedResults<PurlSummary>>, AppError>` and the service layer now constructs `PurlSummary` with qualifier-free PURLs. The `without_qualifiers()` method is documented in the Implementation Notes as part of the `PackageUrl` builder in `common/src/purl.rs`.
