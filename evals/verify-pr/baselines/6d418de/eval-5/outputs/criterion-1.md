# Criterion 1: `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

## Verdict: PASS

## Reasoning

The code changes in `modules/fundamental/src/purl/service/mod.rs` introduce qualifier stripping via `p.without_qualifiers()` followed by `simplified.to_string()` in the PURL serialization. This transforms the output from fully-qualified PURLs (e.g., `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar`) to versioned PURLs without qualifiers (e.g., `pkg:maven/org.apache/commons-lang3@3.12`).

The `without_qualifiers()` method is referenced in the task's Implementation Notes as an existing method on the `PackageUrl` builder in `common/src/purl.rs`, confirming this is the intended approach.

The test `test_recommend_purls_basic` in `tests/api/purl_recommend.rs` explicitly asserts:
```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This confirms the endpoint returns versioned PURLs without qualifiers.

Additionally, the qualifier join (`JoinType::LeftJoin, purl::Relation::PurlQualifier.def()`) was removed from both the endpoint handler (unused import removed) and the service query, ensuring qualifiers are no longer fetched from the database.

## Evidence

- `modules/fundamental/src/purl/service/mod.rs`: `.map(|p| { let simplified = p.without_qualifiers(); PurlSummary { purl: simplified.to_string() } })`
- `modules/fundamental/src/purl/endpoints/recommend.rs`: Removed `use sea_orm::JoinType;`
- `tests/api/purl_recommend.rs`: `assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");`
