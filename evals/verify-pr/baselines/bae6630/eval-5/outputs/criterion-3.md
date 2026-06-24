# Criterion 3: Duplicate entries are deduplicated after qualifier removal

## Acceptance Criterion
Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response.

## Analysis

### Implementation Changes

In `modules/fundamental/src/purl/service/mod.rs`, after stripping qualifiers with `without_qualifiers()`, the code applies deduplication:

```rust
.dedup_by(|a, b| a.purl == b.purl)
```

This removes consecutive duplicate entries where the simplified PURL string matches. Since qualifiers were stripped, two PURLs that were previously distinct (e.g., same version but different `repository_url` qualifiers) will now have identical string representations and be collapsed into one entry.

Note: `dedup_by` only removes *consecutive* duplicates, which works correctly here because the query results are ordered (by the database query), so identical versioned PURLs will be adjacent.

The count query was also updated to use `group_by(purl::Column::Id)` with `select_only()` to ensure the total count reflects the deduplicated result set.

### Test Coverage

The new `test_recommend_purls_dedup` test in `tests/api/purl_recommend.rs` explicitly verifies this behavior:
- Seeds two PURLs for the same package version with different qualifiers (`repo1.maven.org` vs `repo2.maven.org`)
- Asserts that only one entry is returned after deduplication: `assert_eq!(body.items.len(), 1)`
- Asserts the returned PURL is the simplified version: `assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12")`

### Verdict

**PASS** -- The implementation applies `dedup_by` on the simplified PURL strings, and the new `test_recommend_purls_dedup` test directly validates that previously-distinct qualifier variants are collapsed into a single entry.
