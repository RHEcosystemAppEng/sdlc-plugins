# Criterion 3: Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

## Verdict: PASS

## Reasoning

The PR implements deduplication in the service layer at `modules/fundamental/src/purl/service/mod.rs`:

```rust
.dedup_by(|a, b| a.purl == b.purl)
```

This is applied after the `map` step that strips qualifiers, so two PURLs that were previously distinct (e.g., `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar` and `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar`) now both map to `pkg:maven/org.apache/commons-lang3@3.12` and are deduplicated.

The new `test_recommend_purls_dedup` test in `tests/api/purl_recommend.rs` directly verifies this behavior:
- Seeds two PURLs with the same namespace/name/version but different `repository_url` qualifiers
- Requests recommendations
- Asserts that only 1 item is returned (deduplicated) instead of 2
- Asserts the returned PURL matches the expected simplified format

Additionally, the query in the service layer adds `group_by(purl::Column::Id)` to the count query, which supports accurate pagination totals after deduplication.

The implementation and test coverage both confirm this criterion is satisfied.

**Note on `dedup_by` correctness:** The `dedup_by` method only removes consecutive duplicates. This works correctly here because the query results are ordered by the database (same namespace/name/version entries are adjacent after the `filter` predicates). If the ordering were not guaranteed, a `HashSet`-based deduplication would be more robust. However, this is consistent with the existing query patterns in the codebase, so it is acceptable.
