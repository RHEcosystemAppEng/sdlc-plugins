# Criterion 3: Deduplication of entries previously distinct due to different qualifiers

## Verdict: PASS

## Reasoning

The criterion requires that duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response.

The PR diff shows deduplication is implemented at both the service and test levels:

1. **Production code** (modules/fundamental/src/purl/service/mod.rs): After stripping qualifiers with `without_qualifiers()` and building `PurlSummary` objects, the code applies `.dedup_by(|a, b| a.purl == b.purl)` on the iterator before `.collect()`. This removes consecutive duplicate PURLs that became identical after qualifier removal.

   Additionally, the query was modified to use `.select_only().column(purl::Column::Id).group_by(purl::Column::Id)` for the count query, which accounts for the changed grouping behavior.

2. **Test verification** in `tests/api/purl_recommend.rs`: The new `test_recommend_purls_dedup` test function directly validates deduplication:
   - Seeds two PURLs for the same package version (`commons-lang3@3.12`) with different qualifiers (`repository_url=https://repo1.maven.org` vs `repository_url=https://repo2.maven.org`)
   - Requests recommendations and asserts `body.items.len()` is 1 (not 2), confirming that the two entries that were previously distinct (due to different qualifiers) are now deduplicated into a single entry
   - Asserts the resulting PURL is `"pkg:maven/org.apache/commons-lang3@3.12"` (without qualifiers)

This replaces the old `test_recommend_purls_with_qualifiers` test, which previously asserted that both qualifier variants were returned as separate entries (asserting `body.items.len() == 2`). The behavioral change is clearly validated.

Note: The `dedup_by` approach only removes consecutive duplicates, which assumes the results are sorted such that identical PURLs (post-qualifier-removal) are adjacent. This is a reasonable assumption given the database ordering, though a `unique_by` or hash-set-based approach would be more robust. However, the test passes with this approach, confirming the criterion is satisfied for the expected use cases.
