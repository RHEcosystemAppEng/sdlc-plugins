## Criterion 4: Filter integrates with existing pagination -- filtered results are paginated correctly

### Verdict: PASS

### Reasoning

The PR correctly integrates license filtering with the existing pagination mechanism:

1. **Filter-before-paginate ordering:** In `modules/fundamental/src/package/service/mod.rs`, the license filter is applied to the query **before** the pagination logic executes:
   - First, the license filter adds a WHERE clause and JOIN (if licenses are provided)
   - Then, `total = query.clone().count(&self.db).await?` counts the filtered results
   - Finally, the query applies offset/limit to return the paginated slice

   This ordering ensures that `total` reflects the count of filtered results (not all packages), and the offset/limit operate on the filtered set.

2. **Consistent with existing pattern:** The implementation follows the same pattern used by other list endpoints in the codebase (e.g., `advisory/endpoints/list.rs`). The `PackageListParams` struct carries `offset: Option<i64>` and `limit: Option<i64>` alongside the new `license` field, and all three are passed through to the service layer.

3. **PaginatedResults wrapper:** The response uses `PaginatedResults<PackageSummary>` from `common/src/model/paginated.rs`, which includes both the paginated `items` and the `total` count. The `total` field reflects the filtered count, enabling clients to compute total pages.

4. **Test coverage:** The `test_list_packages_license_filter_with_pagination` integration test directly verifies this criterion:
   - Seeds 5 MIT-licensed packages and 1 Apache-2.0 package (6 total)
   - Sends `GET /api/v2/package?license=MIT&limit=2&offset=0`
   - Asserts `body.items.len() == 2` (respects the limit parameter)
   - Asserts `body.total == 5` (total reflects filtered count, not all 6 packages)

   This confirms both that pagination parameters work with the filter and that the total count is correct for the filtered set.

### Evidence

- `mod.rs`: License filter applied before `query.clone().count()` and pagination
- `mod.rs`: Method signature: `list(&self, offset: Option<i64>, limit: Option<i64>, license_filter: Option<&[String]>)`
- `list.rs`: All three params forwarded: `.list(params.offset, params.limit, license_filter.as_deref())`
- Test: `test_list_packages_license_filter_with_pagination` asserts `items.len() == 2` and `total == 5`
