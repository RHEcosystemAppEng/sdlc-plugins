## Criterion 3: Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

**Result: PASS**

### Analysis

The PR implements deduplication in `modules/fundamental/src/purl/service/mod.rs` using `.dedup_by(|a, b| a.purl == b.purl)` in the iterator chain after qualifier removal. This ensures that PURLs which were previously distinct only because of different qualifiers (e.g., `commons-lang3@3.12?repository_url=repo1` vs `commons-lang3@3.12?repository_url=repo2`) are collapsed into a single entry.

The new test `test_recommend_purls_dedup` in `tests/api/purl_recommend.rs` directly validates this behavior:
- Seeds two PURLs with the same namespace/name/version but different `repository_url` qualifiers
- Asserts that only 1 item is returned (not 2)
- Asserts the returned PURL matches the versioned form without qualifiers: `pkg:maven/org.apache/commons-lang3@3.12`

Note: `dedup_by` only removes consecutive duplicates, which works correctly here because the query results are ordered, so identical versioned PURLs (after qualifier removal) will be adjacent. The query's existing sort order ensures this adjacency.

The count query was also updated with `group_by(purl::Column::Id)` and `select_only().column(purl::Column::Id)` to ensure the total count reflects unique entries.
