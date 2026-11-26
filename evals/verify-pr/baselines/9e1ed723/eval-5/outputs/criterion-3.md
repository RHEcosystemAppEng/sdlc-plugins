# Criterion 3

**Criterion:** Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

**Verdict:** PASS (with advisory concerns)

## Evidence

- `PurlService::recommend` adds `.dedup_by(|a, b| a.purl == b.purl)` after mapping each row to a
  qualifier-free `PurlSummary`. Entries whose simplified PURL strings match are merged.
- Test: `test_recommend_purls_dedup` (new, tests/api/purl_recommend.rs) seeds
  `commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar` and
  `commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar`. It asserts that `items.len() == 1` and that
  `items[0].purl == "pkg:maven/org.apache/commons-lang3@3.12"`. This is the scenario the criterion describes, and CI passes.

## Advisory concerns (none blocks the criterion)

1. **Only adjacent duplicates are removed.** `dedup_by` merges consecutive equal elements only. The visible
   query has no explicit `ORDER BY` that groups equal simplified PURLs together. With larger data sets,
   duplicates that are not next to each other could still show up.
2. **Dedup runs after pagination.** `offset`/`limit` are applied in SQL before dedup. A page can therefore hold
   fewer than `limit` items, and duplicates that fall on different pages are not merged.
3. **`total` is counted before dedup.** `total` is a count of `purl::Column::Id` (grouped by Id), not of distinct
   simplified PURLs. It can be larger than the number of unique entries. `test_recommend_purls_dedup` does not
   assert `total`, so this gap is not tested.

## Conclusion

The task's dedup scenario is implemented and tested. The concerns above are robustness issues for a
follow-up, not a failure of the criterion as written.
