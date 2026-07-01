## Criterion 1: `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

**Result: PASS**

### Analysis

The PR modifies the service layer in `modules/fundamental/src/purl/service/mod.rs` to strip qualifiers from returned PURLs. Specifically:

1. The qualifier join (`JoinType::LeftJoin, purl::Relation::PurlQualifier.def()`) is removed from the recommendation query.
2. The mapping step now calls `p.without_qualifiers()` to produce a simplified PURL before converting to string.
3. The `PurlSummary.purl` field is populated with `simplified.to_string()`, which produces a versioned PURL without the `?key=value` qualifier suffix.

The endpoint handler in `modules/fundamental/src/purl/endpoints/recommend.rs` continues to return `Json<PaginatedResults<PurlSummary>>`, so the endpoint path and HTTP method are unchanged.

The test `test_recommend_purls_basic` in the PR confirms this behavior: it seeds PURLs with qualifiers (`?repository_url=...&type=jar`) and asserts that the response contains `pkg:maven/org.apache/commons-lang3@3.12` (versioned, no qualifiers). The additional `assert!(!body.items[0].purl.contains('?'))` further validates no qualifier parameters are present.

The new test file `tests/api/purl_simplify.rs` also validates this behavior across multiple PURL types (npm, pypi) and edge cases (no version).
