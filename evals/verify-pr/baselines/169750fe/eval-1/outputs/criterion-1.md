# Criterion 1: Single License Filter

**Criterion:** `GET /api/v2/package?license=MIT` returns only packages with MIT license

**Verdict:** PASS

## Evidence

The diff in `modules/fundamental/src/package/endpoints/list.rs` adds a `license` field to `PackageListParams`:

```rust
pub license: Option<String>,
```

When present, the `validate_license_param` function splits the comma-separated string and validates each identifier via `Expression::parse`. The validated identifiers are passed to `PackageService::list()` as `license_filter`.

In `modules/fundamental/src/package/service/mod.rs`, the `list` method applies the filter using SeaORM's `is_in` query:

```rust
if let Some(licenses) = license_filter {
    query = query.filter(
        Condition::any()
            .add(package_license::Column::License.is_in(licenses.iter().cloned()))
    );
    query = query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def());
}
```

For a single license like `?license=MIT`, the `split(',')` produces a single-element vector `["MIT"]`, which is passed to `is_in`. The `InnerJoin` with `PackageLicense` ensures only packages with a matching license record are returned.

The integration test `test_list_packages_single_license_filter` in `tests/api/package.rs` confirms this behavior: it seeds packages with MIT and Apache-2.0 licenses, filters by MIT, and asserts that only 2 MIT packages are returned with `assert!(body.items.iter().all(|p| p.license == "MIT"))`.

**Conclusion:** The implementation correctly filters packages by a single SPDX license identifier.
