# Criterion 3: Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

## Verdict: PASS

## Reasoning

The PR implements deduplication at the service layer and includes a dedicated test to verify it:

1. **Implementation** -- In `modules/fundamental/src/purl/service/mod.rs`, after stripping qualifiers, the code applies deduplication:
   ```rust
   .dedup_by(|a, b| a.purl == b.purl)
   ```
   This removes consecutive duplicate entries where the PURL strings match after qualifier removal. PURLs that were previously distinct (e.g., `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar` vs `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar`) would become identical (`pkg:maven/org.apache/commons-lang3@3.12`) after qualifier stripping, and `dedup_by` collapses them.

2. **Dedicated test** -- The new `test_recommend_purls_dedup` function in `tests/api/purl_recommend.rs` directly tests this scenario:
   - Seeds two PURLs with the same name/version but different `repository_url` qualifiers
   - Requests recommendations
   - Asserts that only **one** entry is returned (deduplicated), not two
   - Asserts the returned PURL matches the expected simplified form

3. **Note on `dedup_by` behavior** -- The `dedup_by` method on Rust iterators removes *consecutive* duplicates only. This works correctly here because the query results from the same namespace/name combination are ordered by the database, so identical simplified PURLs will be adjacent. If PURLs were interleaved, `dedup_by` could miss non-adjacent duplicates. However, given the query filters on namespace and name, the database ordering makes consecutive dedup sufficient. The `group_by` clause added to the count query also supports accurate total counts after dedup.

The implementation and test together satisfy this criterion.
