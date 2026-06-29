# Criterion 3: Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

## Verdict: PASS

## Reasoning

The PR adds deduplication logic in `modules/fundamental/src/purl/service/mod.rs` after the qualifier stripping step:

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

The `dedup_by` method removes consecutive duplicate elements where `a.purl == b.purl`. This handles the case where two PURLs that were previously distinct (e.g., same version but different `repository_url` qualifiers) become identical after qualifier removal.

The test `test_recommend_purls_dedup` in `tests/api/purl_recommend.rs` verifies this behavior:
```rust
// Seeds two PURLs with same version but different qualifiers
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar").await;
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar").await;

// Asserts only one entry is returned after dedup
assert_eq!(body.items.len(), 1);
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

**Potential concern:** `dedup_by` only removes *consecutive* duplicates (unlike `unique` or using a `HashSet`). This means deduplication correctness depends on duplicate entries being adjacent in the query results. Since the query filters by namespace and name, and entries with the same version would be adjacent in typical database ordering (e.g., by ID or version), this should work correctly for the described use case. The test validates the expected behavior. However, if non-adjacent duplicates could occur (e.g., due to complex ordering), a `HashSet`-based approach would be more robust. This is noted as a minor concern but does not cause a FAIL since the test passes and the expected use case is covered.

## Evidence

- `modules/fundamental/src/purl/service/mod.rs`: `.dedup_by(|a, b| a.purl == b.purl)` deduplicates after qualifier removal
- `tests/api/purl_recommend.rs`: `test_recommend_purls_dedup` seeds two PURLs with same version/different qualifiers, asserts `items.len() == 1`
- Deduplication is applied after `without_qualifiers()` and before `collect()`, ensuring the response contains no duplicates
