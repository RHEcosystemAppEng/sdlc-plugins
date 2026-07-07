# Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

## Verdict: PASS

## Analysis

The diff adds a `license` query parameter to the `PackageListParams` struct in `list.rs`:

```rust
pub license: Option<String>,
```

When the `license` parameter is provided, the handler calls `validate_license_param(license)` which splits on commas and validates each identifier via `spdx::Expression::parse()`. For a single license like `MIT`, this produces a `Vec<String>` with one element.

The validated identifiers are passed to `PackageService::list()` as `license_filter: Option<&[String]>`. In `service/mod.rs`, when the filter is present, the service applies:

```rust
if let Some(licenses) = license_filter {
    query = query.filter(
        Condition::any()
            .add(package_license::Column::License.is_in(licenses.iter().cloned()))
    );
    query = query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def());
}
```

This produces a SQL `WHERE license IN ('MIT')` with an INNER JOIN on the `package_license` table, restricting results to only packages with a matching MIT license.

The test `test_list_packages_single_license_filter` in `tests/api/package.rs` verifies this:
- Seeds 3 packages (2 MIT, 1 Apache-2.0)
- Queries `?license=MIT`
- Asserts 200 OK, 2 items returned, all with license == "MIT"

## Evidence

- `list.rs`: `pub license: Option<String>` field added to `PackageListParams`
- `list.rs`: `validate_license_param()` function validates SPDX identifiers
- `service/mod.rs`: `license_filter` parameter added, `is_in` filter applied
- `tests/api/package.rs`: `test_list_packages_single_license_filter` verifies behavior
