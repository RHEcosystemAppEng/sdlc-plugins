# Criterion 1: `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

## Verdict: PASS

## Reasoning

The PR modifies the service layer (`modules/fundamental/src/purl/service/mod.rs`) to strip qualifiers from PURLs before returning them in the response. Specifically:

1. **Qualifier join removed:** The `JoinType::LeftJoin` on `purl::Relation::PurlQualifier` has been removed from the query, so qualifier data is no longer fetched from the database.

2. **`without_qualifiers()` applied:** In the `.map()` closure, each PURL entity is transformed via `p.without_qualifiers()` before being serialized to a string. The task's Implementation Notes confirm that the `PackageUrl` builder in `common/src/purl.rs` supports this method. This ensures that only the type, namespace, name, and version components are included in the output.

3. **Test verification:** The `test_recommend_purls_basic` test now asserts:
   - `assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12")` -- this is a versioned PURL without qualifiers.
   - The test seeds PURLs with qualifiers (`?repository_url=...&type=jar`) but expects them returned without qualifiers.

4. **New test file confirmation:** The `test_simplified_purl_no_version` and `test_simplified_purl_mixed_types` tests in `purl_simplify.rs` further confirm that PURLs of various types are returned without qualifiers after seeding with qualified PURLs.

5. **Endpoint unchanged:** The endpoint handler at `modules/fundamental/src/purl/endpoints/recommend.rs` still serves `GET /api/v2/purl/recommend` with the same route structure, only the service layer behavior changed.

The code change directly implements this criterion and the tests confirm it works correctly. CI passes, providing runtime confirmation.
