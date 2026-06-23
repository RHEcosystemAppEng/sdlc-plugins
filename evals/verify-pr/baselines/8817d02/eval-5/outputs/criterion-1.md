# Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

**Criterion:** `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

**Verdict:** PASS

## Reasoning

The PR modifies both the service layer and the endpoint to strip qualifiers from the response:

1. **Service layer change (`modules/fundamental/src/purl/service/mod.rs`):** The `recommend` method now calls `p.without_qualifiers()` on each result before constructing the `PurlSummary`. The previous implementation used `p.to_string()` directly, which included qualifiers. The new implementation calls `let simplified = p.without_qualifiers(); PurlSummary { purl: simplified.to_string() }`, ensuring qualifiers are stripped.

2. **Query change (`modules/fundamental/src/purl/service/mod.rs`):** The `JoinType::LeftJoin` on `purl::Relation::PurlQualifier` has been removed from the query. This join was only needed for qualifier inclusion in the response. Removing it means qualifier data is no longer fetched from the database.

3. **Endpoint change (`modules/fundamental/src/purl/endpoints/recommend.rs`):** The `use sea_orm::JoinType` import was removed, confirming the join is no longer used at the endpoint level.

4. **Test confirmation (`tests/api/purl_recommend.rs`):** The `test_recommend_purls_basic` test now asserts `body.items[0].purl` equals `"pkg:maven/org.apache/commons-lang3@3.12"` (versioned, no qualifiers). The old assertion expected `"pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar"` (with qualifiers).

5. **New test confirmation (`tests/api/purl_simplify.rs`):** Multiple new tests verify the simplified format across different PURL types (maven, npm, pypi), all asserting that returned PURLs do not contain qualifiers.

The code changes directly implement the criterion: the endpoint now returns versioned PURLs (e.g., `pkg:maven/org.apache/commons-lang3@3.12`) without qualifier strings appended.
