# Criterion 3: Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

## Verdict: PASS

## Analysis

When qualifiers are stripped, PURLs that were previously distinct (e.g., same package version but different `repository_url` qualifiers) become identical strings. Without deduplication, the response would contain duplicate entries.

**Implementation evidence:**
- In `modules/fundamental/src/purl/service/mod.rs`, after the `.map()` closure strips qualifiers, a `.dedup_by(|a, b| a.purl == b.purl)` call is chained before `.collect()`. This removes consecutive duplicate PURL strings from the results.
- The count query is also modified to use `.select_only().column(purl::Column::Id).group_by(purl::Column::Id)` to ensure the total count reflects unique entries.

**Test evidence:**
- `test_recommend_purls_dedup` (new function in `tests/api/purl_recommend.rs`) explicitly tests this scenario:
  - Seeds two PURLs for the same package version with different qualifiers (`repository_url=https://repo1.maven.org` and `repository_url=https://repo2.maven.org`)
  - Asserts `body.items.len() == 1` (deduplicated to one entry)
  - Asserts the single entry equals `"pkg:maven/org.apache/commons-lang3@3.12"` (the versioned form without qualifiers)

**Note on dedup_by correctness:** The `dedup_by` method removes consecutive duplicates. This works correctly here because the query results are ordered (same namespace, name, version grouping), so duplicate PURLs (differing only by qualifiers that are now stripped) will be adjacent. If results were not ordered, non-consecutive duplicates could survive. The existing pagination and sorting behavior preserves ordering, making `dedup_by` sufficient.

The implementation addresses the deduplication requirement, and a dedicated test confirms the expected behavior.
