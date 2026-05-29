# Criterion 1: `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

## Verdict: PASS

## Reasoning

The PR modifies the recommendation endpoint in two key locations to ensure versioned PURLs are returned without qualifiers:

1. **`modules/fundamental/src/purl/service/mod.rs`** -- The service layer now calls `p.without_qualifiers()` on each PURL before serializing it:
   ```rust
   .map(|p| {
       let simplified = p.without_qualifiers();
       PurlSummary {
           purl: simplified.to_string(),
       }
   })
   ```
   This strips all qualifier key-value pairs from the PURL string, leaving only the scheme, type, namespace, name, and version components.

2. **`modules/fundamental/src/purl/endpoints/recommend.rs`** -- The `JoinType` import for `sea_orm::JoinType` was removed, indicating the qualifier join is no longer used in the query pipeline.

3. **Test evidence confirms this behavior:**
   - `test_recommend_purls_basic` seeds PURLs with qualifiers (`?repository_url=...&type=jar`) but asserts the response contains `pkg:maven/org.apache/commons-lang3@3.12` (no qualifiers).
   - `test_recommend_purls_basic` also asserts `!body.items[0].purl.contains('?')` and `!body.items[1].purl.contains('?')`, directly verifying no qualifier separator is present.
   - `test_recommend_purls_dedup` also confirms the response PURL is `pkg:maven/org.apache/commons-lang3@3.12` without qualifiers.

The code changes directly implement this criterion by using the `without_qualifiers()` method on the `PackageUrl` builder (as described in the implementation notes) and the tests validate the expected output format.
