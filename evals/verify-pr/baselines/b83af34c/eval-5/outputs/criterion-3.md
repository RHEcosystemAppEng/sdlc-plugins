# Criterion 3: Deduplication after qualifier removal

## Acceptance Criterion

> Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

## Verdict: PASS

## Analysis

### Implementation Evidence

The PR adds deduplication logic in `modules/fundamental/src/purl/service/mod.rs`:

```rust
.dedup_by(|a, b| a.purl == b.purl)
```

This is applied after the `map` step that strips qualifiers, so PURLs that were previously distinct due to different qualifiers (e.g., same package version with `repository_url=repo1` vs `repository_url=repo2`) now compare as equal and are deduplicated.

The `dedup_by` method removes consecutive duplicate elements. Since the results come from a database query ordered by the same columns, identical PURLs (post-qualifier-stripping) will be adjacent, making consecutive deduplication effective.

### Query Change Evidence

The PR also removes the qualifier join from the query:

```rust
// Before:
.join(JoinType::LeftJoin, purl::Relation::PurlQualifier.def());
// After: join removed entirely
```

Removing the qualifier join means the query no longer produces separate rows for different qualifiers of the same PURL, which reduces the deduplication burden. The `dedup_by` call handles any remaining cases where the same versioned PURL appears multiple times.

### Test Evidence

The new test function `test_recommend_purls_dedup` in `tests/api/purl_recommend.rs` directly validates this behavior:

1. Seeds two PURLs with the same version but different qualifiers:
   - `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar`
   - `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar`

2. Requests recommendations and asserts:
   - `assert_eq!(body.items.len(), 1)` -- only one entry returned (deduplicated)
   - `assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12")` -- the deduplicated PURL has no qualifiers

This test directly mirrors the acceptance criterion scenario -- two entries previously distinct due to different qualifiers are now collapsed into one.

### Conclusion

The implementation correctly deduplicates entries after qualifier removal using `dedup_by`, and the dedicated test `test_recommend_purls_dedup` validates the expected behavior with a concrete example of qualifier-based deduplication.
