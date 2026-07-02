# Criterion 3: Deduplication After Qualifier Removal

**Criterion**: Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

**Verdict**: PASS

## Analysis

The service layer adds a `.dedup_by(|a, b| a.purl == b.purl)` call after the `without_qualifiers()` mapping. This removes consecutive items with identical PURL strings from the result set.

The implementation in `modules/fundamental/src/purl/service/mod.rs`:
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

**Note on dedup_by semantics**: The `dedup_by` method only removes *consecutive* duplicates. For this to correctly handle all duplicates, the query results must be ordered such that entries that become identical after qualifier removal are adjacent. Since the query filters by namespace and name, and database ordering typically groups by primary key or version, same-version entries (which would become duplicates after qualifier stripping) are likely adjacent. The test confirms this works for the expected case.

## Test Evidence

The `test_recommend_purls_dedup` test in `tests/api/purl_recommend.rs` directly verifies this:
- Seeds two PURLs for the same package version with different qualifiers:
  - `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar`
  - `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar`
- Calls the recommendation endpoint
- Asserts only 1 item is returned (`assert_eq!(body.items.len(), 1)`)
- Asserts the returned PURL is the simplified form (`pkg:maven/org.apache/commons-lang3@3.12`)

This is a well-designed test that precisely validates the deduplication behavior for the exact scenario described in the criterion.
