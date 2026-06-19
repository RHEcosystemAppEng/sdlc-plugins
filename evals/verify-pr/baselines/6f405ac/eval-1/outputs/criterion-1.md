# Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

## Verdict: PASS

## Reasoning

The PR adds a `license` query parameter to the `PackageListParams` struct in `modules/fundamental/src/package/endpoints/list.rs`:

```rust
pub struct PackageListParams {
    pub offset: Option<i64>,
    pub limit: Option<i64>,
    pub license: Option<String>,
}
```

When the `license` parameter is present, it is validated via `validate_license_param()` which parses each identifier using `spdx::Expression::parse()`. The validated identifiers are then passed to `PackageService::list()` as `license_filter: Option<&[String]>`.

In `modules/fundamental/src/package/service/mod.rs`, the service method applies the filter:

```rust
if let Some(licenses) = license_filter {
    query = query.filter(
        Condition::any()
            .add(package_license::Column::License.is_in(licenses.iter().cloned()))
    );
    query = query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def());
}
```

This filters packages via an INNER JOIN to the `package_license` table, selecting only rows where the license column matches one of the provided identifiers. For a single value like `MIT`, the `is_in` clause effectively becomes an equality check, returning only MIT-licensed packages.

The integration test `test_list_packages_single_license_filter` in `tests/api/package.rs` seeds packages with MIT and Apache-2.0 licenses, queries with `?license=MIT`, and asserts that only 2 packages are returned, all with `license == "MIT"`.

## Evidence

- `list.rs`: `PackageListParams` includes `pub license: Option<String>`
- `list.rs`: `validate_license_param` parses and validates the license string
- `list.rs`: `list_packages` handler passes `license_filter` to `PackageService::list()`
- `service/mod.rs`: `is_in(licenses.iter().cloned())` filter with INNER JOIN on PackageLicense
- `tests/api/package.rs`: `test_list_packages_single_license_filter` asserts correct filtering behavior
