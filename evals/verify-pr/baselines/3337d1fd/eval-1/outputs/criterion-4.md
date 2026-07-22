## Criterion 4: Filter integrates with existing pagination -- filtered results are paginated correctly

### Verdict: PASS

### Reasoning

This criterion requires that the license filter works correctly alongside the existing pagination parameters (`offset` and `limit`), producing properly paginated filtered results.

**Filter-then-paginate ordering (`mod.rs`):**
The filter is applied to the query before pagination:
```rust
if let Some(licenses) = license_filter {
    query = query.filter(
        Condition::any()
            .add(package_license::Column::License.is_in(licenses.iter().cloned()))
    );
    query = query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def());
}

let total = query.clone().count(&self.db).await?;

let items = query
```
The `total` count is computed from the filtered query (after the `if let Some` block), ensuring it reflects only the filtered result set. The pagination (`offset`/`limit`) is then applied to the same filtered query for fetching items. This means:
1. The filter narrows the dataset
2. `total` counts the filtered rows
3. `offset`/`limit` paginate within the filtered set

This is the correct ordering -- filter first, then paginate. If pagination were applied before filtering, the `total` and page boundaries would be wrong.

**Existing pagination infrastructure:**
The `PackageListParams` struct retains `offset: Option<i64>` and `limit: Option<i64>` alongside the new `license` field. The pagination logic in the `list` method (applying offset/limit to the query and wrapping in `PaginatedResults`) was not modified -- only the filter was inserted before it.

**Test coverage (`tests/api/package.rs`):**
The test `test_list_packages_license_filter_with_pagination` provides a thorough verification:
1. Seeds 5 MIT-licensed packages and 1 Apache-2.0 package
2. Sends `GET /api/v2/package?license=MIT&limit=2&offset=0`
3. Asserts:
   - Status is 200 OK
   - `body.items.len() == 2` (limit is respected on filtered results)
   - `body.total == 5` (total reflects all MIT packages, not all 6 packages)

The assertion on `body.total == 5` is particularly important -- it confirms that the total count is computed from the filtered set (5 MIT packages), not the unfiltered set (6 total packages). This validates that the `PaginatedResults` wrapper correctly reports the filtered total.

### Evidence

- `mod.rs`: Filter applied before `query.clone().count()` and pagination, ensuring correct total and page boundaries
- `list.rs`: `PackageListParams` retains existing `offset` and `limit` fields alongside new `license` field
- `tests/api/package.rs`: `test_list_packages_license_filter_with_pagination` asserts `items.len() == 2` and `total == 5` (5 MIT out of 6 total, paginated to 2)
