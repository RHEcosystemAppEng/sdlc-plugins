## Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

**Result: PASS**

### Evidence

The PR adds a `license` query parameter to the `PackageListParams` struct in `modules/fundamental/src/package/endpoints/list.rs`:

```rust
pub struct PackageListParams {
    pub offset: Option<i64>,
    pub limit: Option<i64>,
    pub license: Option<String>,
}
```

When a `license` parameter is present, the handler calls `validate_license_param` which parses the comma-separated string, then passes the result to `PackageService::list()`. In `modules/fundamental/src/package/service/mod.rs`, the service applies a filter:

```rust
if let Some(licenses) = license_filter {
    query = query.filter(
        Condition::any()
            .add(package_license::Column::License.is_in(licenses.iter().cloned()))
    );
    query = query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def());
}
```

This uses an `is_in` filter on the `package_license` table's `License` column with an inner join, ensuring only packages matching the provided license identifiers are returned.

The integration test `test_list_packages_single_license_filter` in `tests/api/package.rs` seeds packages with MIT and Apache-2.0 licenses, then queries `?license=MIT` and asserts that only 2 items are returned and all have license "MIT":

```rust
assert_eq!(body.items.len(), 2);
assert!(body.items.iter().all(|p| p.license == "MIT"));
```

The implementation correctly handles single license filtering.
