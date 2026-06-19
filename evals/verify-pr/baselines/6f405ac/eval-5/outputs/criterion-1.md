# Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

## Verdict: PASS

## Reasoning

The criterion requires that `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers.

The PR diff shows changes in two production files that accomplish this:

1. **modules/fundamental/src/purl/service/mod.rs**: The service layer was modified to strip qualifiers from PURLs before returning them. The key change is:
   - The `JoinType::LeftJoin` on `purl::Relation::PurlQualifier` was removed, meaning qualifier data is no longer fetched from the database.
   - The `.map()` closure now calls `p.without_qualifiers()` to produce a simplified PURL, and constructs `PurlSummary` from `simplified.to_string()` instead of `p.to_string()`.

2. **modules/fundamental/src/purl/endpoints/recommend.rs**: The `sea_orm::JoinType` import was removed (no longer needed since the qualifier join was dropped).

3. **tests/api/purl_recommend.rs**: The `test_recommend_purls_basic` test was updated to assert that the response contains `"pkg:maven/org.apache/commons-lang3@3.12"` (versioned, without qualifiers) instead of the previous fully qualified PURL with `?repository_url=...&type=jar`. The test comment was updated from "fully qualified PURLs" to "versioned PURLs without qualifiers".

The code changes correctly implement the endpoint behavior described in this criterion. The endpoint still accepts the same query parameter and returns versioned PURLs, but now strips qualifier details from the response.
