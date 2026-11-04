# Criterion 4: Filter integrates with existing pagination; filtered results are paginated correctly

**Verdict: PASS**

## Code evidence
- In `PackageService::list`, the license filter and join are applied to `query` before the existing `let total = query.clone().count(&self.db).await?;` line and before the existing offset/limit item fetch. The total count and the returned page therefore come from the same filtered query.
- `offset` and `limit` are still passed straight through from `PackageListParams`, so the existing pagination path is reused without change.
- When no license is given (`None`), no filter or join is added, so unfiltered pagination behaves exactly as before.

## Test evidence
- `tests/api/package.rs::test_list_packages_license_filter_with_pagination` seeds 5 MIT packages and 1 Apache-2.0 package, requests `?license=MIT&limit=2&offset=0`, and asserts status 200, `items.len() == 2`, and `total == 5`. This confirms that the page is limited and that `total` reflects the filtered set, not all packages.

## Notes (non-blocking)
- The concern from criterion 2 applies here too: if one package can match several license rows, the count would include join duplicates. Selecting distinct packages, or using an `EXISTS` subquery, would remove that risk. With the single-license-per-package data the tests use, pagination is correct.
- The test covers only the first page (`offset=0`).
