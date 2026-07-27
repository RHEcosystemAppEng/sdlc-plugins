# Criterion 4: Filter integrates with existing pagination -- filtered results are paginated correctly

## Verdict: PASS

## Reasoning

### What the criterion requires

When the license filter is applied alongside pagination parameters (`offset` and `limit`), the filtered results must be paginated correctly: the `items` array should contain at most `limit` items from the filtered set, and the `total` field should reflect the full count of filtered (not unfiltered) results.

### Evidence from the diff

**1. Filter applied before pagination (service/mod.rs)**

In the `PackageService::list` method, the license filter is applied to the query builder before the pagination logic:

```rust
let mut query = Package::find();

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

The ordering is critical: the filter is applied to `query`, then `query.clone().count()` computes the total count of filtered results, and then pagination (offset/limit) is applied to the same filtered query for fetching items. This ensures `total` reflects the filtered count, not the unfiltered count.

**2. Pagination parameters preserved (list.rs)**

The handler passes `params.offset` and `params.limit` alongside the license filter to the service:

```rust
.list(params.offset, params.limit, license_filter.as_deref())
```

The existing pagination logic in the service method (applying offset and limit to the query) operates on the already-filtered query, so pagination slices the filtered result set.

**3. Test coverage (tests/api/package.rs)**

The test `test_list_packages_license_filter_with_pagination` directly verifies this criterion:
- Seeds 5 MIT-licensed packages and 1 Apache-2.0 package (6 total)
- Calls `GET /api/v2/package?license=MIT&limit=2&offset=0`
- Asserts exactly 2 items returned (respecting `limit=2`)
- Asserts `body.total == 5` (total reflects all 5 MIT packages, not 6 total packages)

This test confirms both that the limit is applied to the filtered set and that the total count correctly reflects the filtered count.

### Conclusion

The filter is applied before the count and item-fetch queries, ensuring that pagination operates on the filtered result set. The total count reflects filtered results, and the limit/offset parameters slice the filtered set correctly. The integration test confirms the expected pagination behavior with filtering. The criterion is satisfied.
