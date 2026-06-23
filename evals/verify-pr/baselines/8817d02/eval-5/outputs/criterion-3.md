# Criterion 3: Duplicate entries deduplicated after qualifier removal

**Criterion:** Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

**Verdict:** PASS

## Reasoning

The PR implements deduplication at the service layer and validates it with a dedicated test:

1. **Deduplication implementation (`modules/fundamental/src/purl/service/mod.rs`):** After mapping each PURL to its simplified (qualifier-free) form, the code applies `.dedup_by(|a, b| a.purl == b.purl)` on the collected results. This removes consecutive duplicate entries where the `purl` field is identical. Since qualifiers have been stripped, PURLs that were previously distinct only due to different qualifier values (e.g., `...@3.12?repository_url=repo1` vs `...@3.12?repository_url=repo2`) now produce the same string (`...@3.12`) and are deduplicated.

2. **Count query updated:** The count query was also modified to use `select_only()`, `column(purl::Column::Id)`, and `group_by(purl::Column::Id)` to produce an accurate total count that accounts for deduplication.

3. **Dedicated test (`test_recommend_purls_dedup` in `tests/api/purl_recommend.rs`):** This new test function directly validates the criterion:
   - Seeds two PURLs for the same package/version but with different qualifier values (`repository_url=repo1` vs `repository_url=repo2`)
   - Requests recommendations
   - Asserts `body.items.len() == 1` (deduplicated to a single entry)
   - Asserts the single result equals `"pkg:maven/org.apache/commons-lang3@3.12"` (qualifier-free)

4. **Contrast with base-branch behavior:** The removed `test_recommend_purls_with_qualifiers` test in the base branch verified the opposite -- that two PURLs with different qualifiers produced 2 separate entries. The new `test_recommend_purls_dedup` verifies they now produce 1 entry.

Note: `dedup_by` only removes consecutive duplicates. This works correctly here because the database query results are ordered, so identical PURLs (after qualifier removal) will be adjacent. If the ordering were not guaranteed, `dedup_by` could miss non-consecutive duplicates. However, the existing ordering from the database query ensures correctness for this use case.

The criterion is satisfied: duplicates arising from qualifier differences are deduplicated.
