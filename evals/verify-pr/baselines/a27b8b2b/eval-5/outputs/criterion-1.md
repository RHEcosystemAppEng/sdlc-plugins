# Criterion 1: GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3 returns versioned PURLs without qualifiers

## Verdict: PASS

## Analysis

The PR modifies two source files to achieve this behavior:

**modules/fundamental/src/purl/endpoints/recommend.rs:**
- The endpoint handler signature remains unchanged, still serving `GET /api/v2/purl/recommend` with `RecommendParams` query extraction.
- The unused `use sea_orm::JoinType;` import is removed, consistent with the removal of the qualifier join in the service layer.

**modules/fundamental/src/purl/service/mod.rs:**
- The `recommend` method no longer joins `purl::Relation::PurlQualifier`, removing qualifier data from the query result set.
- The mapping closure now calls `p.without_qualifiers()` before serialization: `let simplified = p.without_qualifiers(); PurlSummary { purl: simplified.to_string() }`.
- This ensures the returned PURL string is the versioned form without qualifiers (e.g., `pkg:maven/org.apache/commons-lang3@3.12` instead of `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar`).

**Test verification:**
- `test_recommend_purls_basic` asserts `body.items[0].purl` equals `"pkg:maven/org.apache/commons-lang3@3.12"` (versioned, no qualifiers).
- The test seeds PURLs with qualifiers but asserts the response contains only the versioned form.

The code change directly implements this criterion: the service layer strips qualifiers from all returned PURLs before constructing the response.
