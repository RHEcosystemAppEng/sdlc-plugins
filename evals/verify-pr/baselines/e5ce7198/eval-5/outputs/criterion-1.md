## Criterion 1: `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

**Result: PASS**

The PR modifies `test_recommend_purls_basic` in `tests/api/purl_recommend.rs` to assert:
```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This confirms the endpoint returns a versioned PURL (`@3.12`) without any qualifiers (no `?repository_url=...&type=jar`).

The production code in `modules/fundamental/src/purl/service/mod.rs` calls `p.without_qualifiers()` on each result before serializing, which strips qualifier parameters from the PURL string. The endpoint handler in `recommend.rs` removes the `JoinType` import and the qualifier join, confirming the query no longer fetches qualifier data.

Additionally, the new test file `tests/api/purl_simplify.rs` includes `test_simplified_purl_no_version` and `test_simplified_purl_mixed_types` which further validate that the endpoint returns PURLs without qualifiers across different PURL types.
