# Criterion 1: Versioned PURLs Without Qualifiers

**Criterion:** `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

**Verdict:** PASS

## Reasoning

The PR modifies the service layer in `modules/fundamental/src/purl/service/mod.rs` to strip qualifiers from the PURL response. Specifically:

1. The qualifier join has been removed:
   - Base: `.join(JoinType::LeftJoin, purl::Relation::PurlQualifier.def())`
   - PR: join removed entirely

2. The PURL serialization now calls `without_qualifiers()`:
   ```rust
   .map(|p| {
       let simplified = p.without_qualifiers();
       PurlSummary {
           purl: simplified.to_string(),
       }
   })
   ```

3. The unused `use sea_orm::JoinType;` import was removed from the endpoint file.

4. The test `test_recommend_purls_basic` asserts the expected behavior:
   ```rust
   assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
   ```

The implementation correctly strips qualifiers from the PURL before including it in the response, producing versioned PURLs (e.g., `pkg:maven/org.apache/commons-lang3@3.12`) instead of fully qualified PURLs (e.g., `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar`).
