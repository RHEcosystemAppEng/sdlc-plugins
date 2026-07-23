# Criterion 3: Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

## Verdict: PASS

## Reasoning

### Code Change Analysis

The PR adds explicit deduplication logic in `modules/fundamental/src/purl/service/mod.rs`:

```rust
.dedup_by(|a, b| a.purl == b.purl)
```

This is applied after the `.map()` that strips qualifiers via `without_qualifiers()`. The chain is:
1. Fetch PURLs from DB (may have same base PURL with different qualifiers)
2. Map each to its qualifier-free representation
3. Deduplicate adjacent entries with identical `purl` strings
4. Collect into the result vector

Previously, PURLs like `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar` and `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar` were distinct entries. After qualifier stripping, both become `pkg:maven/org.apache/commons-lang3@3.12` and the `.dedup_by()` collapses them to a single entry.

### Query Layer Change

The service also modifies the count query to use `group_by(purl::Column::Id)` with `select_only()` and `column(purl::Column::Id)`, which adjusts how the total count is computed. The qualifier join (`JoinType::LeftJoin, purl::Relation::PurlQualifier.def()`) is removed entirely since qualifiers are no longer needed.

### Test Verification

The new `test_recommend_purls_dedup` function in `tests/api/purl_recommend.rs` directly tests this:
- Seeds two PURLs with the same base but different qualifiers (different `repository_url` values)
- Requests recommendations
- Asserts only 1 item is returned (`assert_eq!(body.items.len(), 1)`)
- Asserts the returned PURL is the deduplicated version without qualifiers

This directly replaces the old `test_recommend_purls_with_qualifiers` test, which previously asserted 2 separate entries were returned for the same scenario. The behavioral change is correctly reflected in the test.

### Conclusion

The `.dedup_by()` call after qualifier stripping ensures duplicate entries are collapsed. The dedicated dedup test verifies this behavior. The criterion is satisfied.
