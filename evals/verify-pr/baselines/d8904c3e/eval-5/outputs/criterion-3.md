## Criterion 3: Deduplication of entries previously distinct due to qualifiers

**Criterion:** Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

**Verdict:** PASS

### Reasoning

**Problem context:** Before this PR, PURLs with the same namespace, name, and version but different qualifiers (e.g., different `repository_url` values) were returned as separate entries. After stripping qualifiers, these would become identical strings, resulting in duplicate entries in the response.

**Implementation verification (`modules/fundamental/src/purl/service/mod.rs`):**

The PR adds a `.dedup_by()` call after the qualifier stripping:

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

This chains `.dedup_by()` after `.map()`, comparing the simplified PURL strings. Adjacent duplicates (which arise from the same base PURL with different qualifiers) are collapsed to a single entry.

**Note on dedup_by semantics:** Rust's `Iterator::dedup_by` removes consecutive duplicates. This works correctly here because the query results are ordered by the PURL columns (namespace, name, version), so entries that become duplicates after qualifier removal are adjacent in the result set.

**Test verification (`tests/api/purl_recommend.rs`):**

The new `test_recommend_purls_dedup` test directly validates this behavior:

```rust
// Seeds two PURLs with same version but different qualifiers
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar").await;
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar").await;

// Asserts only one entry is returned
assert_eq!(body.items.len(), 1);
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This test seeds two PURLs that were previously distinct (different `repository_url` qualifiers) and verifies they collapse to a single entry after qualifier removal.

**Conclusion:** The implementation adds `.dedup_by()` to the query pipeline, and the dedicated `test_recommend_purls_dedup` test verifies the deduplication behavior with a concrete scenario. The criterion is satisfied.
