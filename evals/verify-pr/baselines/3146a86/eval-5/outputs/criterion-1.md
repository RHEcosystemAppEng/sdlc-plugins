# Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

## Criterion
`GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers.

## Verdict: PASS

## Reasoning

The PR modifies the service layer (`modules/fundamental/src/purl/service/mod.rs`) to strip qualifiers from PURLs before returning them. Specifically:

1. **Qualifier join removed:** The `JoinType::LeftJoin` on `purl::Relation::PurlQualifier` has been removed from the query, meaning qualifier data is no longer fetched from the database.

2. **`without_qualifiers()` applied:** The mapping logic now calls `p.without_qualifiers()` on each PURL entity before serializing it:
   ```rust
   .map(|p| {
       let simplified = p.without_qualifiers();
       PurlSummary {
           purl: simplified.to_string(),
       }
   })
   ```
   This uses the existing `PackageUrl` builder's `without_qualifiers()` method, as referenced in the Implementation Notes.

3. **Endpoint layer unchanged functionally:** The endpoint handler in `recommend.rs` still returns `Result<Json<PaginatedResults<PurlSummary>>, AppError>` -- only the unused `JoinType` import was removed, which is consistent since the join is no longer used.

4. **Test verification:** The updated `test_recommend_purls_basic` test seeds PURLs with qualifiers (`?repository_url=...&type=jar`) but asserts the response contains the versioned PURL without qualifiers:
   ```rust
   assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
   ```
   This directly validates that the endpoint returns versioned PURLs without qualifiers.

The code changes in the service layer correctly strip qualifiers, the endpoint returns the simplified PURLs, and tests confirm this behavior. This criterion is satisfied.
