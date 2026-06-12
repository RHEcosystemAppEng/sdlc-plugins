## Criterion 4: Filter integrates with existing pagination -- filtered results are paginated correctly

**Verdict:** PASS

### Reasoning

The license filter is applied to the query before pagination is computed. In `service/mod.rs`:

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
    // ... offset/limit applied here
```

The filter and join are applied to `query` before the `total` count is computed. This means:
1. `total` reflects the count of filtered results (only matching packages), not all packages
2. The `items` query also includes the filter, so pagination (offset/limit) is applied to the filtered set

Note on `.filter()` vs `.join()` ordering: SeaORM's query builder accumulates conditions and joins in its internal state. The SQL is generated at execution time, not at the point of each builder call. Both the filter and join are present in the query state before any SQL is executed, so the generated SQL will include the JOIN and WHERE clauses together correctly. This is confirmed by the fact that all CI checks pass, including the pagination integration test.

The integration test `test_list_packages_license_filter_with_pagination` validates this:
- Seeds 5 MIT packages and 1 Apache-2.0 package
- Requests `?license=MIT&limit=2&offset=0`
- Asserts `body.items.len() == 2` (page size is 2)
- Asserts `body.total == 5` (total filtered MIT packages, not all 6 packages)

This confirms that filtering is applied before both the count and the pagination slice.

### Evidence

- `service/mod.rs`: Filter applied to `query` before `query.clone().count()` (total)
- `service/mod.rs`: Same filtered `query` used for paginated item retrieval
- `tests/api/package.rs`: `test_list_packages_license_filter_with_pagination` verifies total=5 with limit=2
- CI status: All checks pass, confirming the query construction is valid at runtime
