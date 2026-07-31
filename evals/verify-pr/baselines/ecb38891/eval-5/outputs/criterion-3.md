# Criterion 3: Duplicate entries deduplicated after qualifier removal

## Verdict: PASS

## Reasoning

The PR implements deduplication of entries that were previously distinct due to different qualifiers:

1. **Dedup implementation:** In `modules/fundamental/src/purl/service/mod.rs`, a `.dedup_by(|a, b| a.purl == b.purl)` call is added to the iterator chain after the qualifier stripping:
   ```rust
   .map(|p| {
       let simplified = p.without_qualifiers();
       PurlSummary {
           purl: simplified.to_string(),
       }
   })
   .dedup_by(|a, b| a.purl == b.purl)
   .collect();
   ```
   This removes consecutive duplicate PURLs that become identical after qualifier removal.

2. **Dedicated dedup test:** The new `test_recommend_purls_dedup` function in `tests/api/purl_recommend.rs` explicitly tests this behavior:
   - Seeds two PURLs with the same namespace/name/version but different `repository_url` qualifiers
   - Asserts that only one entry is returned after deduplication:
     ```rust
     assert_eq!(body.items.len(), 1);
     assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
     ```

3. **Note on dedup_by behavior:** The `dedup_by` method only removes consecutive duplicates. This works correctly because the query results are ordered by the database, so identical PURLs (after qualifier removal) from the same package will be adjacent. The `group_by` clause added to the count query also supports this.

The code changes and dedicated test confirm that deduplication is implemented and verified.
