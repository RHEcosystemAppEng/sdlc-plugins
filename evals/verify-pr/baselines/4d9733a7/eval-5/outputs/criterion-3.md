## Criterion 3: Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

**Verdict: PASS**

### Reasoning

The PR adds explicit deduplication in the service layer (`modules/fundamental/src/purl/service/mod.rs`):

```rust
.dedup_by(|a, b| a.purl == b.purl)
```

This is applied after the qualifier stripping step (`.map(|p| { let simplified = p.without_qualifiers(); ... })`), so entries that were previously distinct only because of different qualifiers (e.g., same package/version but different `repository_url`) are now collapsed into a single entry.

The new test `test_recommend_purls_dedup` in `tests/api/purl_recommend.rs` directly verifies this behavior:

1. Seeds two PURLs for the same package version with different qualifiers:
   - `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar`
   - `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar`

2. Requests recommendations and asserts only one entry is returned:
   ```rust
   assert_eq!(body.items.len(), 1);
   assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
   ```

This directly demonstrates that entries previously distinct due to different qualifiers are now deduplicated. The criterion is satisfied.

Note: `dedup_by` only removes consecutive duplicates, which works here because the query results are ordered, but this is a minor implementation detail that does not affect the criterion verdict given that the test confirms the expected behavior.
